import os
import sys
import shutil
import win32com.client
import subprocess
import datetime
import psutil
import getpass
import socket
import json



config_padrao_dict = {
    "caminho_log_error": r"\\server008\G\ARQ_PATRIMAR\WORK\INVENTARIO\telemetria_patrimar\log_error_instalador.csv",
    "caminho_origem": r"\\server008\G\ARQ_PATRIMAR\WORK\INVENTARIO\telemetria_patrimar\telemetria_patrimar.exe",
    "caminho_destino": r"C:\Telemetria Patrimar",
    "config_origem": r"\\server008\G\ARQ_PATRIMAR\WORK\INVENTARIO\telemetria_patrimar\config.ini",
    "cliente_origem": r"\\server008\G\ARQ_PATRIMAR\WORK\INVENTARIO\telemetria_patrimar\cliente.pickle",
}



def carregar_json():
    '''
    é responsavel por carregar um arquivo json contendo um dicionario com dados de login no sap.
    caso o arquivo não estiver presente durante a execução irá  criar um arquivo default no lugar.
    '''
    while True:
        try:
            with open("config.json", "r")as arqui:
                return json.load(arqui)
        except:
            with open("config.json", "w")as arqui:
                json.dump(config_padrao_dict, arqui)

arquivo = carregar_json()


def verificar_execucao_processo(nome_processo="telemetria_patrimar.exe"):
    for processo in psutil.process_iter(attrs=['pid', 'name']):
        if processo.info['name'] == nome_processo:
            pid = processo.info['pid']
            psutil.Process(pid).terminate()
            return True
    return False


usuario = getpass.getuser()
maquina = socket.gethostname()
def log_error(caminho=arquivo["caminho_log_error"], erro=None):
    with open(caminho, "a")as arqui:
        arqui.write(f"{datetime.datetime.today().strftime('%d/%m/%Y')};{datetime.datetime.today().strftime('%H:%M:%S')};{maquina};{usuario};{erro}\n")


def iniciar():
    # Definir os caminhos dos arquivos
    caminho_origem = arquivo["caminho_origem"].replace('"',"")
    caminho_destino = arquivo["caminho_destino"].replace('"',"")

    caminho_inicializacao = os.path.join(
        os.environ["APPDATA"],
        "Microsoft",
        "Windows",
        "Start Menu",
        "Programs",
        "Startup",
    )

    # Verificar se a pasta de destino existe e criar se não existir
    if not os.path.exists(caminho_destino):
        os.makedirs(caminho_destino)

    # Copiar o arquivo para o caminho de destino
    shutil.copy2(caminho_origem, caminho_destino)
    shutil.copy2(arquivo["config_origem"].replace('"',""), arquivo["caminho_destino"].replace('"',""))
    shutil.copy2(arquivo["cliente_origem"].replace('"',""), arquivo["caminho_destino"].replace('"',""))

    # Criar atalho para o arquivo copiado
    atalho_destino = os.path.join(caminho_inicializacao, "telemetria_patrimar.lnk")
    shell = win32com.client.Dispatch("WScript.Shell")
    atalho = shell.CreateShortCut(atalho_destino)
    atalho.Targetpath = os.path.join(caminho_destino, "telemetria_patrimar.exe")
    atalho.save()

    # Executar o atalho
    if verificar_execucao_processo() == False:
        print(atalho.Targetpath)
        subprocess.Popen(atalho.Targetpath, shell=True)
        print("executou")
        


if __name__ == "__main__":
    try:
        for x in range(3):
            verificar_execucao_processo()
        iniciar()
    except Exception as error:
        print(error)
        log_error(erro=error)
