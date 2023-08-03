import pickle
import os
############# Imports do cliente
import sys
import socket
import getpass
import platform
import psutil
import winreg
import ctypes
import uuid
import datetime
import platform
import subprocess
from time import sleep
import requests
import win32com.client

arquivo = {
    "caminho_log_error": r"\\server008\G\ARQ_PATRIMAR\WORK\INVENTARIO\telemetria_patrimar\log_error_telemetria.csv",
    "caminho_online": r"\\server008\G\ARQ_PATRIMAR\WORK\INVENTARIO\telemetria_patrimar\cliente.pickle",
    "caminho_offline": r"C:\Telemetria Patrimar\cliente.pickle"
}

usuario = getpass.getuser()
maquina = socket.gethostname()
def log_error(caminho=arquivo["caminho_log_error"].replace('"',""), erro=None):
    with open(caminho, "a")as arqui:
        arqui.write(f"{datetime.datetime.today().strftime('%d/%m/%Y')};{datetime.datetime.today().strftime('%H:%M:%S')};{maquina};{usuario};{erro}\n")
class Telemetria:
    def __init__(self, caminhos):
        self.__caminho = caminhos
        if os.path.exists(self.__caminho["online"]):
            self.__codigo = self.online()
        elif os.path.exists(self.__caminho["offline"]):
            self.__codigo = self.offline()
    
    def online(self):
        codigo = ""
        with open(self.__caminho["online"], "rb") as arqui:
            for x in pickle.load(arqui):
                codigo += f"{x}\n"
        with open(self.__caminho["offline"], "wb") as arqui:
            pickle.dump(codigo.split("\n"), arqui)
        return codigo
    
    def offline(self):
        codigo = ""
        with open(self.__caminho["offline"], "rb") as arqui:
            for x in pickle.load(arqui):
                codigo += f"{x}\n"
        return codigo
    
    def executar(self):
        return self.__codigo

if __name__ == "__main__":
    try:
        caminhos = {"online" : arquivo["caminho_online"].replace('"',""), "offline" : arquivo["caminho_offline"].replace('"',"")}
        iniciar = Telemetria(caminhos)
    except KeyError:
        #arquivo = config_padrao()
        caminhos = {"online" : arquivo["caminho_online"].replace('"',""), "offline" : arquivo["caminho_offline"].replace('"',"")}
        iniciar = Telemetria(caminhos)
    except Exception as error:
        print(error)
        try:
            log_error(erro=error)
        except:
            pass
    cont = 0
    while True:
        try:
            exec(iniciar.executar())
        except Exception as error:
            print(error)
            if cont >= 20:
                try:
                    log_error(erro=error)
                except:
                    pass
                cont = 0
            cont += 1
        sleep(5*60)
    