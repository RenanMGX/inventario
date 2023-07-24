##################################################################################
#####     Renan Brian                                                        #####
#####     Especialista em Programação | Transformando ideias em código       #####
#####     E-mail: renanmgx@hotmail.com                                       #####
##################################################################################
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

def obter_informacoes_computador():
    # # Nome do computador
    nome_computador = socket.gethostname()

    # # Nome do usuário
    nome_usuario = getpass.getuser()

    # # Modelo do processador
    modelo_processador = obter_modelo_processador()

    # # Quantidade de RAM
    ram = psutil.virtual_memory().total  # em bytes
    ram_formatada = formatar_tamanho_ram(ram)

    ram_usado = psutil.virtual_memory().used  # em bytes
    ram_usado_formatada = formatar_tamanho_ram(ram_usado)

    # # Sistema operacional
    sistema_operacional = obter_detalhes_sistema_operacional()

    total, disponivel = obter_tamanho_armazenamento()

    tipo_maquina = identificar_tipo_maquina()
    #print(tipo_maquina)

    antivirus = verificar_instalacao_symantec()

    #criptografia = verificar_criptografia_ativada()
    criptografia = False

    id_dispositivo = get_device_id()

    uso_processador = obter_uso_processador()

    nome_rede_wifi = obter_nome_rede_wifi()
    #print(nome_rede_wifi)
    data_atual = datetime.datetime.now()

    modelo_placa_mae = get_motherboard_model()

    numero_seria_placa_mae = get_motherboard_serial_number()

    return {
          "id_dispositivo" : str(id_dispositivo),
          "nome_computador": str(nome_computador),
          "nome_usuario": str(nome_usuario),
          "modelo_processador": str(modelo_processador),
          "ram_total": str(ram_formatada),
          "ram_usado": str(ram_usado_formatada),
          "sistema_operacional": str(sistema_operacional),
          "armazenamento_total": str(total),
          "armazenamento_disponivel": str(disponivel),
          "tipo_maquina" : str(tipo_maquina),
          "antivirus" : str(antivirus),
          "criptografia" : str(criptografia),
          "uso_processador" : str(uso_processador),
          "wifi" : str(nome_rede_wifi),
          "data" : str(data_atual),
          "placa_mae" : str(modelo_placa_mae),
          "placa_mae_serial" : str(numero_seria_placa_mae)
    }

######## funçoes para coletar os dados da maquina
def obter_uso_processador():
    uso_processador = psutil.cpu_percent()
    return uso_processador

def get_motherboard_model():
    try:
        output = subprocess.check_output("wmic baseboard get product", shell=True)
        output = output.decode("utf-8").strip()
        lines = output.split("\n")
        if len(lines) >= 2:
            motherboard_model = lines[1]
            return motherboard_model
    except Exception as e:
        print(f"Ocorreu um erro ao obter o modelo da placa-mãe: {e}")
    return None

def get_motherboard_serial_number():
    obj = win32com.client.GetObject("winmgmts:").InstancesOf("Win32_BaseBoard")
    for item in obj:
        return item.SerialNumber

def obter_nome_rede_wifi():
    if sys.platform == 'win32':
        try:
            comando = 'netsh wlan show interfaces'
            saida = subprocess.run(comando, capture_output=True, shell=True, text=True).stdout
            for linha in saida.split("\n"):
                if "SSID" in linha:
                    nome_rede = linha.split(":")[1].strip()
                    return nome_rede
        except subprocess.CalledProcessError:
            pass
    
    return None

def obter_modelo_processador():
    chave_registro = winreg.OpenKey(
        winreg.HKEY_LOCAL_MACHINE,
        r"HARDWARE\DESCRIPTION\System\CentralProcessor\0"
    )
    modelo, _ = winreg.QueryValueEx(chave_registro, "ProcessorNameString")
    winreg.CloseKey(chave_registro)
    return modelo

def formatar_tamanho_ram(tamanho_bytes):
    for unidade in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if tamanho_bytes < 1024:
            return f"{tamanho_bytes:.2f} {unidade}"
        tamanho_bytes /= 1024

def obter_detalhes_sistema_operacional():
    info = platform.uname()
    sistema_operacional = f"{info.system} {info.release}"

    if info.system == 'Windows':
        version = obter_versao_windows()
        sistema_operacional += f" {version}"

    return sistema_operacional

def obter_versao_windows():
    kernel32 = ctypes.WinDLL('kernel32')
    kernel32.GetSystemWow64DirectoryW.restype = ctypes.c_uint32

    is_64bit = kernel32.GetSystemWow64DirectoryW(None, 0) != 0
    is_server = platform.win32_ver()[0] == 'Server'

    if is_server:
        return "Server"
    elif is_64bit:
        return "64-bit"
    else:
        return "32-bit"

def get_device_id():
    mac = uuid.getnode()
    device_id = '-'.join(("%012X" % mac)[i:i+2] for i in range(0, 12, 2))
    return device_id

def formatar_tamanho(bytes):
    unidades = ['B', 'KB', 'MB', 'GB', 'TB']
    tamanho = bytes
    indice = 0

    while tamanho >= 1024 and indice < len(unidades) - 1:
        tamanho /= 1024
        indice += 1

    return f'{tamanho:.2f} {unidades[indice]}'

def obter_tamanho_armazenamento():
    disco = psutil.disk_usage('C:/')
    tamanho_total = formatar_tamanho(disco.total)
    tamanho_disponivel = formatar_tamanho(disco.free)
    return tamanho_total, tamanho_disponivel

def principal():
    informacoes = obter_informacoes_computador()
    dados = {}
    url = 'http://INVENTARIO:5000/patrimar'
    #url = 'http://127.0.0.1:5000/patrimar'
    for key, value in informacoes.items():
        #print(f"{key} : {value}")
        dados[key] = value
    requests.post(url, json=dados)

def identificar_tipo_maquina():
    system = platform.system()
    if system == "Windows":
        battery = psutil.sensors_battery()
        if battery is not None and battery.power_plugged:
            return "Notebook"
        else:
            return "Desktop"
    else:
        return "Sistema operacional não suportado"

def verificar_instalacao_symantec():
    # Verificar a existência de arquivos associados ao Symantec AntiVirus
    arquivos_symantec = [
        "C:\\Program Files\\Symantec\\Symantec Endpoint Protection\\smc.exe",
        "C:\\Program Files (x86)\\Symantec\\Symantec Endpoint Protection\\smc.exe"
    ]
    for arquivo in arquivos_symantec:
        if subprocess.run(['cmd', '/c', 'dir', arquivo], capture_output=True, shell=True).returncode == 0:
            return True

    # Verificar a existência de entradas no Registro do sistema
    try:
        subprocess.run(['reg', 'query', 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Symantec\\Symantec Endpoint Protection'], capture_output=True, check=True, shell=True)
        return True
    except subprocess.CalledProcessError:
        pass

    try:
        subprocess.run(['reg', 'query', 'HKEY_LOCAL_MACHINE\\SOFTWARE\\WOW6432Node\\Symantec\\Symantec Endpoint Protection'], capture_output=True, check=True, shell=True)
        return True
    except subprocess.CalledProcessError:
        pass

    return False

def verificar_criptografia_ativada():
    comando = 'manage-bde -status C:'
    resultado = subprocess.run(comando, capture_output=True, text=True)
    
    # Verifica se o comando foi executado com sucesso
    if resultado.returncode == 0:
        saida = resultado.stdout
        linhas = saida.split('\n')
        # Verifica se o BitLocker está ativado ou desativado
        for linha in linhas:
            if 'Protection Status:' in linha:
                status = linha.split(':')[1].strip()
                return status
    
    # Retorna None se houver algum erro ou se o BitLocker não estiver ativado
    return None

principal()