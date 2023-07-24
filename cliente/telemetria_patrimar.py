import sys
import os
#### imports criptografados
from time import sleep
from datetime import datetime
import getpass
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

class Telemetria:
    def __init__(self, caminhos):
        self.__caminho = caminhos
        if os.path.exists(self.__caminho["online"]):
            self.__codigo = self.online()
        elif os.path.exists(self.__caminho["offline"]):
            self.__codigo = self.offline()
    
    def descriptografar(self, texto_criptografado, chave):
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
    
    def online(self):
        codigo = ""
        with open(self.__caminho["online"], "r")as arqui:
            codigo = arqui.read()
        with open(self.__caminho["offline"], "w")as arqui:
            arqui.write(codigo)
        return self.descriptografar(codigo,402)
    
    def offline(self):
        codigo = ""
        with open(self.__caminho["offline"], "r")as arqui:
            codigo = arqui.read()
        return self.descriptografar(codigo,402)
    
    def executar(self):
        try:
            exec(self.__codigo)
        except Exception as error:
            print(error)



if __name__ == "__main__":
    caminhos = {"online" : r"\\server008\G\ARQ_PATRIMAR\WORK\INVENTARIO\telemetria_patrimar\cliente.dat",
                "offline": r"C:\telematria_patrimar\cliente.dat"
                }
    programa = Telemetria(caminhos)
    exec(programa.online())

