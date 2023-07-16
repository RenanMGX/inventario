import tkinter as tk
from tkinter import filedialog

def procurar_arquivo():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    return file_path

def criptografar(texto, chave):
    texto_criptografado = ''
    for caractere in texto:
        if caractere.isalpha():
            if caractere.islower():
                novo_caractere = chr((ord(caractere) - 97 + chave) % 26 + 97)
            else:
                novo_caractere = chr((ord(caractere) - 65 + chave) % 26 + 65)
        else:
            novo_caractere = caractere
        texto_criptografado += novo_caractere
    return texto_criptografado



arquivo = procurar_arquivo()
nome_arquivo = arquivo.split("/")
nome_arquivo = nome_arquivo[-1].split(".")
nome_arquivo = nome_arquivo[0] + ".dat"

with open(arquivo, "r") as arqui:
    arquivo = arqui.read()

texto_criptografado = criptografar(arquivo, 402)

with open(nome_arquivo, "w") as arqui:
    arqui.write(texto_criptografado)