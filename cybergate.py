import os
import subprocess
from tkinter import Tk, filedialog
import nmap
from scapy.all import *

# Função para obter os dispositivos disponíveis na rede
def obter_dispositivos_na_rede():
    nm = nmap.PortScanner()
    nm.scan(hosts='192.168.0.0/24', arguments='-sn')  # Substitua pelo intervalo de IP da sua rede

    dispositivos = []
    for host in nm.all_hosts():
        if 'mac' in nm[host]['addresses']:
            mac_address = nm[host]['addresses']['mac']
            dispositivos.append({"ip": host, "mac": mac_address})

    return dispositivos

# Função para listar os dispositivos enumerados
def listar_dispositivos():
    output = subprocess.check_output(['adb', 'devices']).decode('utf-8')
    lines = output.split('\n')[1:]  # Ignora a primeira linha

    dispositivos = []
    for line in lines:
        if line.strip() != '':
            dispositivo = line.split('\t')[0]
            dispositivos.append(dispositivo)

    return dispositivos

# Função para controlar os dispositivos
def controlar_dispositivos():
    dispositivos = obter_dispositivos_na_rede()

    if not dispositivos:
        print("Nenhum dispositivo encontrado na rede.")
        return

    print("Dispositivos disponíveis:")
    for i, dispositivo in enumerate(dispositivos):
        print(f"{i+1}. {dispositivo['ip']} - {dispositivo['mac']}")

    while True:
        escolha = input("Escolha um dispositivo pelo número (0 para sair): ")

        if escolha == "0":
            break

        try:
            indice_dispositivo = int(escolha) - 1
            dispositivo = dispositivos[indice_dispositivo]

            # Lógica para controlar o dispositivo
            print(f"Controlando o dispositivo: {dispositivo['ip']}")
            # Adicione aqui a lógica para controlar o dispositivo com base no endereço IP ou MAC

        except (ValueError, IndexError):
            print("Escolha inválida. Tente novamente.")

# Função para parear o dispositivo com a TV
def parear_tv(dispositivos):
    print("Dispositivos:")
    for i, dispositivo in enumerate(dispositivos):
        print(f"{i+1}. {dispositivo}")

    escolha = input("Escolha o número do dispositivo que deseja parear: ")
    if escolha.isdigit() and int(escolha) <= len(dispositivos):
        dispositivo_escolhido = dispositivos[int(escolha) - 1]
        print(f"Pareando o dispositivo '{dispositivo_escolhido}' com a TV...")
        
        comando = f"adb pair {dispositivo_escolhido}"
        subprocess.run(comando, shell=True)
        
        print("Pareamento realizado com sucesso.")
    else:
        print("Opção inválida.")

# Função para carregar um vídeo
def carregar_video():
    escolha = input("Como você deseja carregar o vídeo?\n1. Por URL\n2. De um arquivo local\nEscolha uma opção: ")

    if escolha == "1":
        url = input("Digite a URL do vídeo: ")
        comando = f"adb loadvideo --url {url}"
        subprocess.run(comando, shell=True)
        print(f"Carregando vídeo por URL: {url}")
    elif escolha == "2":
        root = Tk()
        root.withdraw()

        caminho_arquivo = filedialog.askopenfilename()
        if caminho_arquivo:
            comando = f"adb loadvideo --file {caminho_arquivo}"
            subprocess.run(comando, shell=True)
            print(f"Carregando vídeo do arquivo local: {caminho_arquivo}")
        else:
            print("Nenhum arquivo selecionado.")
    else:
        print("Opção inválida.")

# Função para escanear dispositivos na rede e calcular a distância aproximada
def scan_devices():
    devices = []
    print("Escaneando dispositivos na rede...")
    arp_result = os.popen("arp -a").read()

    for line in arp_result.splitlines():
        if "incomplete" not in line:
            ip, _, mac, _ = line.split()
            devices.append((ip, mac))

    return devices

def get_distance(rssi):
    # Fórmula de cálculo aproximado da distância
    # Pode variar dependendo do ambiente e do dispositivo
    tx_power = -59  # Potência de transmissão do sinal em dBm
    n = 2.7  # Expoente que varia de 2 a 4 dependendo do ambiente
    return 10 ** ((tx_power - rssi) / (10 * n))

def scan_devices():
    devices = []
    print("Escaneando dispositivos na rede...")
    arp_result = os.popen("arp -a").read()

    for line in arp_result.splitlines():
        if "incomplete" not in line:
            ip, _, mac, _ = line.split()
            devices.append((ip, mac))

    return devices

def main():
    devices = scan_devices()

    for index, (ip, mac) in enumerate(devices, 1):
        print(f"Dispositivo {index}:")
        print(f"IP: {ip}")
        print(f"MAC: {mac}")
        rssi = random.randint(-90, -40)  # Simulação de um valor RSSI
        distance = get_distance(rssi)
        print(f"Distância aproximada: {distance} metros")
        print()

if __name__ == "__main__":
    main()
