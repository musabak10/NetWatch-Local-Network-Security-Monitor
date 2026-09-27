# NetWatch

NetWatch is a Python-based local network security monitoring tool designed to discover and track devices on an authorized local network.

It automatically detects the active network configuration, performs ARP-based device discovery, stores device information, and compares scans over time.

## Features

- Automatically detects the local IPv4 address
- Automatically detects the subnet mask
- Automatically detects the default gateway
- Calculates the local network range
- Performs active ARP discovery
- Detects newly discovered devices
- Detects devices that leave the network
- Detects MAC address changes
- Normalizes MAC address formats before comparison
- Stores the latest scan in JSON
- Stores scan history with timestamps

## How It Works

NetWatch first reads the active Wi-Fi network configuration from Windows using `ipconfig`.

The IPv4 address and subnet mask are then used to calculate the local network range.

For example:

```text
IP:       10.58.86.46
Subnet:   255.255.240.0
Network:  10.58.80.0/20
```

NetWatch then sends ARP requests to the calculated local network and records devices that respond.

Each discovered device contains:

```json
{
    "ip": "10.58.80.1",
    "mac": "00:00:0c:9f:f2:9b",
    "type": "dynamic"
}
```

The current scan is compared with the previous scan to detect network changes.

## Detection

NetWatch currently detects three types of changes:

### New Device

A device is considered new when its IP address was not present in the previous scan.

```text
Yeni cihaz bulundu!
IP: 10.58.80.10
MAC: 00:00:5e:00:01:06
```

### Removed Device

A device is considered removed when its IP address was present in the previous scan but is not found in the current scan.

```text
Cihaz ağdan ayrıldı!
IP: 10.58.80.10
MAC: 00:00:5e:00:01:06
```

### MAC Address Change

NetWatch compares the MAC address associated with an IP address between scans.

MAC addresses are normalized before comparison so that formats such as:

```text
00-00-0c-9f-f2-9b
```

and:

```text
00:00:0c:9f:f2:9b
```

are treated as the same address.

## Project Structure

```text
netwatch.py
```

Main application containing network detection, ARP discovery, device comparison, and JSON storage.

```text
devices.json
```

Stores the devices detected during the latest scan.

```text
history.json
```

Stores previous scans together with their timestamps.

```text
requirements.txt
```

Contains the external Python dependency required by the project.

## Installation

Clone the repository:

```bash
git clone https://github.com/musabak10/NetWatch.git
cd NetWatch
```

Install the required package:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python netwatch.py
```

On Windows, Scapy may require Npcap for packet capture and network operations.

## Example Output

```text
IP: 10.58.86.46
Subnet: 255.255.240.0
Gateway: 10.58.80.1
Network: 10.58.80.0/20

ARP taraması yapılıyor...

Yeni cihaz bulundu!
IP: 10.58.80.2
MAC: a0:e0:af:1f:67:00
Type: dynamic

Toplam cihaz: 6
```

## Technologies

- Python
- Scapy
- ARP
- JSON
- IPv4
- Windows networking tools

## Purpose

This project was built as a practical cybersecurity and networking project to understand:

- Local network discovery
- ARP
- IP addressing and subnetting
- MAC addresses
- Network monitoring
- Device tracking
- Basic anomaly detection
- JSON-based data persistence

## Scope

NetWatch is intended for monitoring networks that you own or are explicitly authorized to monitor.

ARP discovery is limited to the local network calculated from the machine's active network configuration. It does not provide visibility into arbitrary remote networks or the entire Internet.

## Future Improvements

Planned improvements may include:

- DNS monitoring
- Event logging
- Device names and vendor identification
- Configurable scan intervals
- Desktop GUI
- Basic anomaly detection
- Port status monitoring
- More detailed network reports

## License

This project is intended for educational and authorized network monitoring purposes.
```
