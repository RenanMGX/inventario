import os
import sys
import pickle
######## imports do script
import shutil
import win32com.client
import subprocess
import datetime
import psutil
import getpass
import socket
###########

class InventarioGPO:
    def __init__(self, arquivo):
        self.__arquivo = arquivo
    
    def decoder(self):
        with open(self.__arquivo, "rb")as arqui:
            arquivo = ""
            for x in pickle.load(arqui):
                arquivo += f"{x}\n"
        return arquivo


if __name__ == "__main__":
    try:
        programa = InventarioGPO("code.pickle")
        exec(programa.decoder())
    except Exception as error:
        print(error)
        pass
