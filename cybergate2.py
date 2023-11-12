import os
import subprocess
import random

# avisa quando há um dispositivo novo

# Verifica e instala as dependências
try:
    import nmap
except ImportError:
    subprocess.run(["pip", "install", "python-nmap"])
    import nmap

try:
    from plyer import notification
except ImportError:
    subprocess.run(["pip", "install", "plyer"])
    from plyer import notification

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

def notify_new_devices(existing_devices, new_devices):
    new_device_count = len(new_devices)
    if new_device_count > 0:
        title = "Novos Dispositivos Encontrados"
        message = f"Foram encontrados {new_device_count} novo(s) dispositivo(s) na rede."
        notification.notify(
            title=title,
            message=message,
            app_name="Device Scanner"
        )

        print("Novos dispositivos encontrados:")
        for index, (ip, mac) in enumerate(new_devices, 1):
            print(f"Dispositivo {index}:")
            print(f"IP: {ip}")
            print(f"MAC: {mac}")
            rssi = random.randint(-90, -40)  # Simulação de um valor RSSI
            distance = get_distance(rssi)
            print(f"Distância aproximada: {distance} metros")
            print()

def main():
    existing_devices = scan_devices()

    while True:
        input("Pressione Enter para escanear novamente...")
        new_devices = scan_devices()
        notify_new_devices(existing_devices, new_devices)
        existing_devices = new_devices

if __name__ == "__main__":
    main()