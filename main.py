import platform
import socket
import uuid
import psutil
import wmi
import pandas as pd
import os
from datetime import datetime

# Informações básicas
hostname = socket.gethostname()
usuario = os.getlogin()
ip = socket.gethostbyname(hostname)
mac = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff)
                for ele in range(0, 8*6, 8)][::-1])

# Sistema operacional
sistema = platform.system()
versao_so = platform.version()
release = platform.release()

# Processador
processador = platform.processor()

# Memória RAM
ram_total = round(psutil.virtual_memory().total / (1024**3), 2)

# Armazenamento
disco = psutil.disk_usage('/')
armazenamento_total = round(disco.total / (1024**3), 2)

# WMI para fabricante e modelo
c = wmi.WMI()
for system in c.Win32_ComputerSystem():
    fabricante = system.Manufacturer
    modelo = system.Model

# Criando estrutura de dados
dados = {
    "Hostname": hostname,
    "Usuario Logado": usuario,
    "Sistema Operacional": sistema,
    "Release": release,
    "Versão SO": versao_so,
    "Processador": processador,
    "Memória RAM (GB)": ram_total,
    "Armazenamento Total (GB)": armazenamento_total,
    "IP": ip,
    "MAC Address": mac,
    "Fabricante": fabricante,
    "Modelo": modelo,
    "Data Coleta": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
}

# Convertendo para DataFrame
df = pd.DataFrame([dados])

# Salvando no Excel
nome_arquivo = f"inventario_{hostname}.xlsx"
df.to_excel(nome_arquivo, index=False)

print(f"Inventário salvo em: {nome_arquivo}")