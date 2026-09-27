import subprocess
import ipaddress
import json
import os

from datetime import datetime
from scapy.all import ARP, Ether, srp


def get_networkinfo():
    result = subprocess.run(
        ["ipconfig"],
        capture_output=True
    )

    output = result.stdout.decode(errors="replace")
    lines = output.splitlines()

    wifi_found = False

    ip = None
    subnet = None
    gateway = None

    for line in lines:

        if "Wireless LAN adapter Wi-Fi:" in line:
            wifi_found = True

        elif wifi_found and line and not line.startswith(" "):
            break

        elif wifi_found:

            if "IPv4 Address" in line:
                ip = line.split(":")[-1].strip()

            elif "Subnet Mask" in line:
                subnet = line.split(":")[-1].strip()

            elif "Default Gateway" in line:
                gateway = line.split(":")[-1].strip()

    return ip, subnet, gateway


def get_arp_table(network):
    arp = ARP(pdst=str(network))
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")

    packet = ether / arp

    answered = srp(
        packet,
        timeout=2,
        verbose=False
    )[0]

    devices = []

    for sent, received in answered:
        devices.append({
            "ip": received.psrc,
            "mac": received.hwsrc,
            "type": "dynamic"
        })

    return devices


def save_devices(devices):
    with open("devices.json", "w") as file:
        json.dump(devices, file, indent=4)


def load_devices():
    if not os.path.exists("devices.json"):
        return []

    with open("devices.json", "r") as file:
        return json.load(file)


def normalize_mac(mac):
    return mac.replace("-", ":").lower()


def find_new_devices(old_devices, new_devices):
    old_ips = {
        device["ip"]
        for device in old_devices
    }

    new_devices_found = []

    for device in new_devices:

        if device["ip"] not in old_ips:
            new_devices_found.append(device)

    return new_devices_found


def find_removed_devices(old_devices, new_devices):
    new_ips = {
        device["ip"]
        for device in new_devices
    }

    removed_devices = []

    for device in old_devices:

        if device["ip"] not in new_ips:
            removed_devices.append(device)

    return removed_devices


def find_mac_changes(old_devices, new_devices):
    old_devices_dict = {
        device["ip"]: normalize_mac(device["mac"])
        for device in old_devices
    }

    mac_changes = []

    for device in new_devices:

        ip = device["ip"]
        new_mac = normalize_mac(device["mac"])

        if ip in old_devices_dict:

            old_mac = old_devices_dict[ip]

            if old_mac != new_mac:
                mac_changes.append({
                    "ip": ip,
                    "old_mac": old_mac,
                    "new_mac": new_mac
                })

    return mac_changes


def save_history(devices):
    history = []

    if os.path.exists("history.json"):
        with open("history.json", "r") as file:
            history = json.load(file)

    history.append({
        "timestamp": datetime.now().isoformat(),
        "devices": devices
    })

    with open("history.json", "w") as file:
        json.dump(history, file, indent=4)


ip, subnet, gateway = get_networkinfo()

interface = ipaddress.ip_interface(
    f"{ip}/{subnet}"
)

print("IP:", ip)
print("Subnet:", subnet)
print("Gateway:", gateway)
print("Network:", interface.network)

print("\nARP taraması yapılıyor...\n")

old_devices = load_devices()

new_devices = get_arp_table(interface.network)

new_devices_found = find_new_devices(
    old_devices,
    new_devices
)

for device in new_devices_found:

    print("Yeni cihaz bulundu!")
    print("IP:", device["ip"])
    print("MAC:", device["mac"])
    print("Type:", device["type"])
    print()


removed_devices = find_removed_devices(
    old_devices,
    new_devices
)

for device in removed_devices:

    print("Cihaz ağdan ayrıldı!")
    print("IP:", device["ip"])
    print("MAC:", device["mac"])
    print()


mac_changes = find_mac_changes(
    old_devices,
    new_devices
)

for change in mac_changes:

    print("MAC adresi değişti!")
    print("IP:", change["ip"])
    print("Eski MAC:", change["old_mac"])
    print("Yeni MAC:", change["new_mac"])
    print()


save_devices(new_devices)
save_history(new_devices)

print(f"Toplam cihaz: {len(new_devices)}")
