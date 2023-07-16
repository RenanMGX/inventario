##################################################################################
#####     Renan Brian                                                        #####
#####     Especialista em Programação | Transformando ideias em código       #####
#####     E-mail: renanmgx@hotmail.com                                       #####
##################################################################################

import os
import shutil
import win32com.client
import subprocess
from datetime import datetime
import psutil
import getpass
import socket

nome_user = getpass.getuser()

def verificar_execucao_processo(nome_processo="telemetria_patrimar.exe"):
    for processo in psutil.process_iter(['name']):
        if processo.info['name'] == nome_processo:
            return True
    return False


# Verifica se o processo está em execução



def iniciar():
    # Definir os caminhos dos arquivos
    caminho_origem = [r"\\server008\G\ARQ_PATRIMAR\WORK\INVENTARIO\telemetria_patrimar\telemetria_patrimar.exe",r"\\server008\G\ARQ_PATRIMAR\WORK\INVENTARIO\telemetria_patrimar\cliente.dat"]
    caminho_destino = f"C:\\telematria_patrimar\\"
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
    for x in caminho_origem:
        shutil.copy2(x, caminho_destino)

    # Criar atalho para o arquivo copiado
    atalho_destino = os.path.join(caminho_inicializacao, "telemetria_patrimar.lnk")
    shell = win32com.client.Dispatch("WScript.Shell")
    atalho = shell.CreateShortCut(atalho_destino)
    atalho.Targetpath = os.path.join(caminho_destino, "telemetria_patrimar.exe")
    atalho.save()

    # Executar o atalho
    if verificar_execucao_processo() == False:
        subprocess.Popen(atalho_destino, shell=True)

try:
    iniciar()
except Exception as error:
    nome_maquina = socket.gethostname()
    hora = str(datetime.now())
    log_error = f"Nome Computador: {nome_maquina}; \n Nome Usuario: {nome_user}; \n Data: {hora}; \n Error: {error} \n ##################################################### \n"
    try:
        with open("\\\\server008\\G\\ARQ_PATRIMAR\\WORK\\INVENTARIO\\log.txt","a") as arqui:
            arqui.write(log_error)
    except:
        pass
