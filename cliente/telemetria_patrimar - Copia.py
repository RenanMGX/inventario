import sys
from time import sleep
from datetime import datetime
import getpass
import sys
import os
import socket
import getpass
import platform
import psutil
import winreg
import ctypes
import uuid
import platform
import subprocess
from time import sleep
import requests
import win32com.client

data_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")


def descriptografar(texto_criptografado, chave):
    texto_descriptografado = ''
    for caractere in texto_criptografado:
        if caractere.isalpha():
            if caractere.islower():
                novo_caractere = chr((ord(caractere) - 97 - chave) % 26 + 97)
            else:
                novo_caractere = chr((ord(caractere) - 65 - chave) % 26 + 65)
        else:
            novo_caractere = caractere
        texto_descriptografado += novo_caractere
    return texto_descriptografado

arquivo  = ""
nome_user = getpass.getuser()
caminho_destino = f"C:\\telematria_patrimar\\cliente.dat"
caminho_destino2 = f"C:\\telematria_patrimar\\"
caminho_destino_servidor = f"\\\\server008\\G\\ARQ_PATRIMAR\\WORK\\INVENTARIO\\telemetria_patrimar\\cliente.dat"

if not os.path.exists(caminho_destino2):
    os.makedirs(caminho_destino2)


try:
    with open(caminho_destino_servidor, "r") as arqui:
        arquivo = arqui.read()
        with open(caminho_destino,"w") as atualizar:
            atualizar.write(arquivo)
except:
    try:
        with open(caminho_destino, "r") as arqui:
            arquivo = arqui.read()
    except Exception as error:
        with open("C:\\telematria_patrimar\\log_error_telemetria_patrimar.txt" , "a") as arqui:
            arqui.write(f"{data_atual}: {error} \n")
        sys.exit()

descriptografado = descriptografar(arquivo, 402)
descriptografado_2 = descriptografado
while True:
    try:
        exec(descriptografado_2)
    except Exception as error:
        print(error)
    sleep(5*60)
