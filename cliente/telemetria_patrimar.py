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
############
class Telemetria:
    def __init__(self, caminhos):
        self.__caminho = caminhos
        if os.path.exists(self.__caminho["online"]):
            self.__codigo = self.online()
        elif os.path.exists(self.__caminho["offline"]):
            print("offline")
    
    def online(self):
        codigo = ""
        with open(self.__caminho["online"], "rb") as arqui:
            codigo = pickle.load(arqui)
           # for x in pickle.load(arqui):
            #    codigo += f"{x}\n"
        with open(self.__caminho["offline"], "wb") as arqui:
            pickle.dump(codigo, arqui)
        return codigo
    
    def executar(self):
        try:
            for x in self.__codigo:
                print(x)
                #exec(x)
        except Exception as error:
            print(error)
            

    



if __name__ == "__main__":
    caminhos = {"online" : r"\\server008\G\ARQ_PATRIMAR\WORK\INVENTARIO\telemetria_patrimar\cliente.pickle", "offline" : r"C:\telematria_patrimar\cliente.pickle"}
    iniciar = Telemetria(caminhos)
    iniciar.executar()
    

