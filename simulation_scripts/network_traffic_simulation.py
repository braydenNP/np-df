from scapy.all import *
import random
import time
import threading
import logging

# Log file for traffic simulation
LOG_FILE = "network_traffic_log.txt"
PCAP_FILE = "network_traffic.pcap"

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Legitimate and malicious domains and IPs
legitimate_domains = ["www.google.com", "www.bankofamerica.com", "www.wikipedia.org"]
malicious_domains = ["www.fakebank.com", "www.cryptowallet.com"]
malicious_ips = ["203.0.113.25", "198.51.100.14"]

captured_packets = []

def generate_legitimate_traffic():
    """Generate DNS and HTTP traffic for legitimate domains."""
    for _ in range(20):
        domain = random.choice(legitimate_domains)
        packet = IP(dst="8.8.8.8") / UDP(dport=53) / DNS(rd=1, qd=DNSQR(qname=domain))
        send(packet, verbose=False)
        captured_packets.append(packet)
        logging.info(f"Legitimate DNS query to {domain}")
        time.sleep(random.uniform(1, 3))

def generate_malicious_traffic():
    """Generate DNS and HTTP traffic for malicious domains."""
    for _ in range(10):
        domain = random.choice(malicious_domains)
        ip = random.choice(malicious_ips)

        # Simulate DNS poisoning
        dns_packet = IP(dst=ip) / UDP(dport=53) / DNS(rd=1, qd=DNSQR(qname=domain))
        send(dns_packet, verbose=False)
        captured_packets.append(dns_packet)
        logging.warning(f"Malicious DNS query to {domain}")

        # Simulate fake login attempt
        login_packet = IP(dst=ip) / TCP(dport=80) / Raw(
            load=f"POST /login HTTP/1.1\r\nHost: {domain}\r\nContent-Length: 25\r\n\r\nusername=admin&password=12345"
        )
        send(login_packet, verbose=False)
        captured_packets.append(login_packet)
        logging.warning(f"Fake login attempt to {domain}")

        time.sleep(random.uniform(2, 5))

def run_traffic_simulation():
    """Run both legitimate and malicious traffic simulations."""
    logging.info("Starting network traffic simulation...")
    threads = [
        threading.Thread(target=generate_legitimate_traffic),
        threading.Thread(target=generate_malicious_traffic),
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    # Save packets to PCAP
    wrpcap(PCAP_FILE, captured_packets)
    logging.info(f"Network traffic simulation completed. PCAP saved to {PCAP_FILE}")

if __name__ == "__main__":
    run_traffic_simulation()
