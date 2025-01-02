# Attack Scenario Overview

This repository contains a set of scripts designed to simulate a sophisticated multi-faceted cyberattack on Evergreen Trust Bank. Below is a detailed description of each script, what it does, and how it relates to the attack scenario.

This suite of scripts works together to simulate the attack scenario with a high degree of realism. Each script creates artifacts and evidence that align with specific stages of the attack, enabling investigators to reconstruct the incident and identify the perpetrator.

## **1. Browser Simulation (`browser_simulation.py`)**

### **What It Does**
1. Simulates DNS cache poisoning by adding a fake bank entry to the `hosts` file, redirecting traffic to a malicious IP.
2. Uses Selenium to mimic browsing activity on financial and cryptocurrency websites, including:
   - Visiting a fake bank.
   - Searching for suspicious terms like "transfer $25,000 to crypto wallet."
   - Visiting dark web forums to mimic money laundering research.
3. Creates temporary files during the browsing session to simulate malware downloads and then deletes them to mimic an attacker covering their tracks.

### **Relation to the Attack Scenario**
- Redirects legitimate banking traffic to a malicious site, aligning with how the attacker might intercept Dr. Wong's credentials.
- Reflects an insider (Michael Tan) researching and executing unauthorized transfers using stolen credentials.
- Provides evidence for investigators in the form of residual artifacts, even after cleanup attempts.

## **2. Phishing Email Simulation (`email_simulation.py`)**

### **What It Does**
1. Creates a fake PDF (`instructions_hidden.pdf`) containing embedded exploit code.
2. Sends phishing emails:
   - **Email 1:** From Rachel Simmons to Michael Tan, instructing him to disable security logging.
   - **Email 2:** A spoofed email, sent from Alan Chow's account to Michael Tan, raising suspicion about Rachel Simmons.
3. Adds forged headers to implicate Alan Chow and mislead investigators.

### **Relation to the Attack Scenario**
- Mimics Rachel Simmons collaborating with Michael Tan to disable critical security features.
- Creates misleading evidence pointing to Alan Chow, adding complexity to the forensic investigation.
- Leaves behind the malicious PDF, which investigators can analyze to uncover its purpose.

## **3. Financial Logs Generator (`generate_financial_logs.py`)**

### **What It Does**
1. Creates a SQLite database with fake transactions involving Dr. Wong, Michael Tan, and Rachel Simmons.
2. Introduces anomalies:
   - Suspicious transfers over $20,000 linked to Michael Tan.
   - Future timestamps to mimic log tampering.
3. Associates transactions with suspicious IPs to indicate unauthorized remote access.

### **Relation to the Attack Scenario**
- Creates realistic financial logs reflecting the unauthorized $25,000 transfer from Dr. Wong's account.
- Links suspicious transactions to Michael Tan and Rachel Simmons through IP addresses and anomalies.
- Provides a rich source of evidence for investigators to analyze patterns and anomalies.

## **4. Event Log Manipulation (`event_log_generator.ps1`)**

### **What It Does**
1. Creates logs for:
   - Login attempts by Michael Tan, Rachel Simmons, and Dr. Wong.
   - Failed login attempts and privilege escalations.
2. Generates logs with realistic but inconsistent timestamps.
3. Simulates log tampering to hide traces of actual events.

### **Relation to the Attack Scenario**
- Reflects Michael Tan's efforts to hide his after-hours access and remote logins.
- Generates fake events to confuse investigators and obscure the timeline of the attack.

## **5. Malware Simulation (`malware_simulator.py`)**

### **What It Does**
1. Simulates ransomware by encrypting sensitive files (e.g., financial documents).
2. Adds a registry key to ensure malware persistence, enabling it to restart after reboots.
3. Retains encrypted files and a hidden encryption key as evidence for investigators.

### **Relation to the Attack Scenario**
- Demonstrates a possible secondary attack vector, targeting sensitive bank data.
- Creates registry entries that investigators can use to trace the malware's origin.
- Provides encrypted files and logs for analysis.

## **6. Network Traffic Simulation (`network_traffic_generator.py`)**

### **What It Does**
1. Uses `scapy` to send packets simulating:
   - DNS requests to the malicious fake bank IP.
   - Data exfiltration to external cryptocurrency wallets.
2. Simulates command-and-control (C2) traffic.

### **Relation to the Attack Scenario**
- Captures traffic patterns showing DNS poisoning and suspicious connections, aligning with the attacker’s actions.
- Provides investigators with a PCAP file that reveals the IPs, domains, and data transfers involved.

## **7. Main Script (`main.py`)**

### **What It Does**
1. Sequentially executes all scripts (browser simulation, email phishing, log manipulation, malware, and network traffic).
2. Adds delays between script executions to mimic real-world attack timelines.
3. Records which scripts ran successfully and any errors encountered.

### **Relation to the Attack Scenario**
- Reflects how the attacker (Michael Tan) systematically executed multiple stages of the attack.
- Provides investigators with timestamps to reconstruct the sequence of events.
- Leaves behind logs that could reveal the attack’s orchestration.