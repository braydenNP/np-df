from scapy.all import *
import random
import time

def generate_network_traffic():
    dest_ips = ["192.168.1.1", "203.0.113.25", "10.0.0.54"]
    ports = [443, 22, 80]

    for _ in range(100):
        packet = IP(dst=random.choice(dest_ips)) / TCP(dport=random.choice(ports), sport=random.randint(1024, 65535)) / Raw(load="Transaction Data: $25,000")
        send(packet)
        time.sleep(random.uniform(0.5, 2))

if __name__ == "__main__":
    generate_network_traffic()
