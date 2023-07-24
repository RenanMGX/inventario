import os
import sys
import shutil
import win32com.client
import subprocess
import datetime
import psutil
import getpass
import socket



config_padrao_dict = {
    "caminho_log_error": r"\\server008\G\ARQ_PATRIMAR\WORK\INVENTARIO\telemetria_patrimar\log_error_instalador.csv",
    "caminho_origem": r"\\server008\G\ARQ_PATRIMAR\WORK\INVENTARIO\telemetria_patrimar\telemetria_patrimar.exe",
    "caminho_destino": r"C:\Telemetria Patrimar",
    "config_origem": r"\\server008\G\ARQ_PATRIMAR\WORK\INVENTARIO\telemetria_patrimar\config.ini",
    "cliente_origem": r"\\server008\G\ARQ_PATRIMAR\WORK\INVENTARIO\telemetria_patrimar\cliente.pickle",
}

def verificar_config():
    try:
        with open("config.ini","r")as arqui:
            arquivo_temp = arqui.read().split("\n")
        arquivo = {}
        for x in arquivo_temp:
            y = x.split(";")
            if len(y) < 2:
                continue
            arquivo[y[0]] = y[1]
        return arquivo
    except Exception as error:
        return False
def config_padrao():
    try:
        with open("config.ini","w")as arqui:
            for x,y in config_padrao_dict.items():
                arqui.write(f'{x};"{y}"\n')
        return config_padrao_dict
    except:
        sys.exit()
arquivo = verificar_config()
if arquivo == False:
    arquivo = config_padrao() 


def verificar_execucao_processo(nome_processo="telemetria_patrimar.exe"):
    for processo in psutil.process_iter(['name']):
        if processo.info['name'] == nome_processo:
            return True
    return False


usuario = getpass.getuser()
maquina = socket.gethostname()
def log_error(caminho=arquivo["caminho_log_error"].replace('"',""), erro=None):
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

try:
    iniciar()
except KeyError:
    arquivo = config_padrao()
    iniciar()
except Exception as error:
    print(error)
    try:
        log_error(erro=error)
    except:
        pass
