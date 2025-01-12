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

# How to Start and Simulate the Attack on the VMs

To simulate the attack scenario using the scripts and tools provided, follow these steps. The process assumes the **Kali Linux VM** is used as the attacker system and the **Windows VM** as the victim system.

## **Setup and Configuration for Simulation**

### **On the Windows Victim VM:**
1. **Install Required Software:**
   - **Python**: Ensure Python 3.x is installed.
   - **PowerShell 7**: Install and configure PowerShell to allow script execution.
     ```powershell
     Set-ExecutionPolicy RemoteSigned
     ```
   - **Google Chrome**: Install Chrome for the browser simulation.
   - **Papercut SMTP**: Configure a local SMTP email server for the phishing simulation.

2. **Download Python Libraries:**
   Run the following command to install required libraries:
   ```bash
   pip install selenium cryptography scapy psutil pywin32
   ```

3. **Enable logging for all successful and failed login attempts, system events, and object access.**
   - Enable logging for all successful and failed login attempts, system events, and object access.
   - Configure it via Local Group Policy:
      ```
      gpedit.msc > Windows Settings > Security Settings > Advanced Audit Policy Configuration
      ```

4. **Directory Structure Setup:** Create the following directories for storing generated evidence:
   ```
   C:\FinancialData
   C:\Users\MichaelTan\AppData\Local
   C:\Logs
   C:\Temp
   ```

5. **Place the Scripts**
      - Place the scripts in appropriate directories, such as:
         ```
         C:\AttackScripts
         ```

6. **Run the `main.py` Script:** Execute the main script to orchestrate all attacks.
      ```bash
      python main.py
      ```

### **On the Windows Victim VM:**
1. **Network Traffic Monitoring:**
   - Open Wireshark or Tshark on Kali to monitor network traffic between VMs.
   - Capture traffic and save it as `network_traffic.pcap`.
     ```bash
     tshark -i eth0 -w network_traffic.pcap
     ```
   - **Google Chrome**: Install Chrome for the browser simulation.
   - **Papercut SMTP**: Configure a local SMTP email server for the phishing simulation.

2. **Prepare Attack Logs and Notes:**
   - Use the Kali VM to craft phishing emails and record timestamps for attacks.

# Simulation Workflow
### Step 1: Infection Phase
   - Simulate DNS poisoning using the `browser_simulation.py` script to redirect banking traffic.
   - Simulate phishing emails using `email_simulation.py` to disable logging and cover tracks.

### Step 2: Data Manipulation Phase
   - Run `generate_financial_logs.py` to create anomalies in financial records..
   - Use `event_log_generator.ps1` to manipulate Windows Event Logs.

### Step 3: Malware and Exfiltration Phase
   - Run `malware_simulator.py` to encrypt sensitive files and add persistence.
   - Simulate data exfiltration with `network_traffic_generator.py` and capture traffic.

# Artifacts Left Behind for Forensic Investigation
1. **Windows Event Logs:**
   - Captured in Security.evtx and System.evtx.

2. **Financial Logs:**
   - SQLite database generated in C:\FinancialData.

3. **Email Artifacts:**
   - Phishing email artifacts in C:\EmailLogs.

4. **Browser Cache:**
   - Found in C:\Users\MichaelTan\AppData\Local\Google\Chrome\User Data\Default.

5. **Network Traffic PCAP:**
   - Saved as network_traffic.pcap on the attacker or defender side.

6. **Encrypted Files:**
   - Found in C:\Temp\Encrypted_Files.

# How to Verify the Simulation
1. **Check Log Files:**
   - Verify `execution_log.txt` to ensure all scripts executed successfully.

2. **Inspect Artifacts:**
   - Examine `Security.evtx` for login anomalies.
   - Open `network_traffic.pcap` in Wireshark to analyze DNS poisoning and data exfiltration.

3. **Reconstruct the Timeline:**
   - Use Plaso (`log2timeline`) to create a forensic timeline of events.

# How to Start Investigation
1. **Collect Artifacts:**
   - Use FTK Imager to create forensic images of the Windows VM.
   - Transfer key files (logs, PCAP, financial data) to the Kali VM for analysis.

2. **Analyze Evidence:**
   - Use Sleuth Kit and Volatility on Kali to analyze memory dumps, disk images, and logs.
   - Cross-reference timestamps in the PCAP file with logs to identify attack patterns.

# File Structure for Kali VM and Windows VM

This document provides a detailed breakdown of the directory structures for both the **Kali (Attacker)** and **Windows (Victim)** VMs used in the attack scenario

## **Kali VM File Structure**
The Kali VM is used as the attacker’s machine to monitor network traffic, analyze evidence, and simulate attack execution.

### **Root Directory**
```plaintext
/home/kali/
```

### **Subdirectories**
1. `/home/kali/evidence/`  
   Used to store evidence collected from the victim system during the investigation.
      ```
   /home/kali/evidence/
   ├── memory_dumps/
   │   └── windows_memory_dump.raw            # Memory dump of the victim VM
   ├── disk_images/
   │   └── victim_disk_image.dd               # Forensic disk image of the victim VM
   ├── network_traffic/
   │   └── network_traffic.pcap               # Captured PCAP file from Wireshark or Tshark
   ├── windows_logs/
   │   ├── Security.evtx                      # Exported security log from the victim VM
   │   └── System.evtx                        # Exported system log from the victim VM
   ├── extracted_artifacts/
   │   ├── email_addresses.txt                # Extracted email addresses
   │   ├── files/
   │   │   ├── suspicious_attachment.pdf      # Extracted attachment from phishing emails
   │   │   └── decrypted_sensitive_file.txt  # Recovered files from encryption
   │   └── registry_analysis.txt              # Extracted registry keys from malware
   ├── timelines/
   │   └── forensic_timeline.csv              # Timeline generated using Plaso/log2timeline
   ├── analysis_reports/
   │   ├── final_report.docx                  # Comprehensive forensic investigation report
   │   ├── screenshots/                       # Screenshots of tools during the analysis
   │   │   ├── volatility_analysis.png
   │   │   └── sleuthkit_file_carving.png
   │   └── findings_summary.txt               # Summary of findings
   ├── decrypted_files/
   │   ├── financial_report.docx              # Files decrypted from ransomware
   │   └── personal_data.txt
   ├── registry_analysis/
   │   └── registry_hive_analyzed.txt         # Registry artifacts analyzed for malicious entries
   ├── process_analysis/
   │   ├── running_processes.txt              # Extracted list of processes from memory analysis
   │   └── malware_signature_analysis.txt     # Identified malicious processes
   ```

12. `/home/kali/tools/`  
Contains tools installed for forensic analysis (not real directory; in built tools).
   ```
   /home/kali/tools/
   ├── volatility/
   ├── sleuthkit/
   ├── tshark/
   ├── bulk_extractor/
   ├── plaso/
   └── dc3dd/
   ```

## **Windows VM File Structure**
The Windows VM is the victim machine where the attack scripts execute and evidence is generated.

### **Root Directory**
```plaintext
C:\
```

### **Subdirectories**
1. `C:\AttackScripts\`  
Contains all attack scripts.
   ```
   C:\AttackScripts\
   ├── browser_activity\
   │   └── browser_simulation.py
   ├── email_simulation\
   │   └── email_generator.py
   ├── financial_logs\
   │   └── generate_financial_logs.py
   ├── log_manipulation\
   │   └── event_log_generator.ps1
   ├── malware_simulation\
   │   └── malware_simulator.py
   ├── network_traffic\
   │   └── network_traffic_generator.py
   └── main.py
   ```

2. `C:\FinancialData\`  
Contains financial logs and sensitive documents targeted by the attack.
   ```
   C:\FinancialData\
   ├── Client_Transactions.xlsx
   ├── Quarterly_Report.docx
   └── Transaction_Logs_Backup.db
   ```

3. `C:\Logs\`  
Stores logs generated by attack scripts or Windows event logs.
   ```
   C:\Logs\
   ├── unauthorized_access.log
   ├── USB_Access_Log.txt
   └── disabled_logging.log
   ```

4. `C:\Temp\`  
Temporary directory used for ransomware encryption and exfiltration simulation.
   ```
   C:\Temp\
   ├── Encrypted_Files\
   │   ├── file_1.txt
   │   ├── file_2.txt
   │   └── file_3.txt
   └── credentials.txt
   ```
5. `C:\Users\MichaelTan\AppData\Local\`  
Hidden files and directories used to simulate malicious activity.
   ```
   C:\Users\MichaelTan\AppData\Local\
   ├── .hidden_wallets\
   │   ├── wallet.dat
   │   └── transaction_log.txt
   ├── .malware_payload\
   │   └── ransomware.exe
   └── .unauthorized_exports\
      ├── Dr_Wong_Transactions.csv
      └── Client_Data_Dump.sql
   ```

6. `C:\EmailLogs\`  
Contains phishing emails sent to and from Michael Tan’s account.
   ```
   C:\EmailLogs\
   ├── phishing_email_1.eml
   └── phishing_email_2.eml
   ```
7. `C:\Windows\Logs\`  
Stores manipulated event logs for investigators.
   ```
   C:\Windows\Logs\
   ├── Security.evtx
   └── System.evtx
   ```
8. `C:\Users\MichaelTan\AppData\Local\Google\Chrome\User Data\Default\`  
Stores browser history and cache files.
   ```
   C:\Users\MichaelTan\AppData\Local\Google\Chrome\User Data\Default\
   ├── History
   └── Cache
   ```

Updated One:
```
C:\Users\<Username>\Documents\
├── FinancialData\
│   ├── Transactions_Backup.db  # Populated
│   ├── Client_Reports.xlsx  # Blank (manual input)
│   ├── Performance_Review.docx  # Blank (manual input)
├── Work_Reports\
│   ├── summary.txt  # Populated
│   ├── log_analysis_report.txt  # Populated
│   ├── encrypted_file_1.txt  # Encrypted
│   ├── encrypted_file_2.txt  # Encrypted

C:\Users\<Username>\AppData\Local\
├── Microsoft\Outlook\
│   ├── internal_review.eml  # Populated
│   ├── q3_analysis_report.eml  # Populated
├── Google\Chrome\User Data\Default\
│   ├── History  # Populated
│   ├── Cache  # Populated

C:\Windows\
├── System32\drivers\etc\
│   ├── hosts  # Modified for DNS poisoning

C:\Logs\
├── network_traffic.pcap  # Populated
```

# Files to Create/Populate for Simulation

| **File Name**                       | **Location**                                         | **Action Needed**       | **Description**                                                                 |
|-------------------------------------|-----------------------------------------------------|-------------------------|---------------------------------------------------------------------------------|
| `Transactions_Backup.db`            | `C:\Users\<Username>\Documents\FinancialData`       | Populated               | Financial database logs for transactions, created/populated by `create_dir.py`. |
| `Client_Reports.xlsx`               | `C:\Users\<Username>\Documents\FinancialData`       | Blank (manual)          | Placeholder for financial client reports.                                       |
| `Performance_Review.docx`           | `C:\Users\<Username>\Documents\FinancialData`       | Blank (manual)          | Placeholder for employee performance review documents.                          |
| `summary.txt`                       | `C:\Users\<Username>\Documents\Work_Reports`        | Populated               | Generated by `create_dir.py`.                                                  |
| `log_analysis_report.txt`           | `C:\Users\<Username>\Documents\Work_Reports`        | Populated               | Contains system analysis data, created by `create_dir.py`.                      |
| `encrypted_file_1.txt`              | `C:\Users\<Username>\Documents\Work_Reports`        | Populated by malware    | File encrypted by `malware_simulator.py`.                                       |
| `encrypted_file_2.txt`              | `C:\Users\<Username>\Documents\Work_Reports`        | Populated by malware    | File encrypted by `malware_simulator.py`.                                       |
| `internal_review.eml`               | `C:\Users\<Username>\AppData\Local\Microsoft\Outlook` | Populated               | Internal email logs populated by `email_generator.py`.                          |
| `q3_analysis_report.eml`            | `C:\Users\<Username>\AppData\Local\Microsoft\Outlook` | Populated               | Populated phishing emails, created by `email_generator.py`.                     |
| `History`                           | `C:\Users\<Username>\AppData\Local\Google\Chrome\User Data\Default` | Populated by browser    | Browsing history generated by `browser_simulation.py`.                          |
| `Cache`                             | `C:\Users\<Username>\AppData\Local\Google\Chrome\User Data\Default` | Populated by browser    | Cache data generated by `browser_simulation.py`.                                |
| `hosts`                             | `C:\Windows\System32\drivers\etc`                  | Modified by browser     | Hosts file modified to simulate DNS poisoning by `browser_simulation.py`.       |
| `audit_log.txt`                     | `C:\Users\<Username>\Documents\Work_Reports`        | Populated by simulation | Audit logs for tracking activities in financial systems.                        |
| `.encryption_key`                   | `C:\Users\<Username>\AppData\Local`                | Populated by malware    | Encryption key file generated by `malware_simulator.py`.                        |
| `network_traffic_log.txt`           | `C:\Users\<Username>\Documents\Logs`               | Populated by simulation | Logs of network traffic generated by `network_traffic_simulator.py`.            |
| `network_traffic.pcap`              | `C:\Users\<Username>\Documents\Logs`               | Populated by simulation | PCAP file containing network packet captures.                                   |
| `malware.log`                       | `C:\Users\<Username>\Documents\Logs`               | Created by simulation   | Log file created by the malware simulator.                                      |
| `EventLog_Security.evtx`            | `C:\Windows\System32\winevt\Logs`                  | Populated by PowerShell | Security event logs generated by `log_manipulation.ps1`.                        |
| `Client_Transactions.xlsx`          | `C:\Users\<Username>\Documents\FinancialData`       | Blank (manual)          | Placeholder file for client transaction data.                                   |
| `memory_dump.raw`                   | `C:\Users\<Username>\Documents\Forensics`          | Manual (via tools)      | Placeholder for system memory dump.                                            |
| `victim_disk_image.dd`              | `C:\Users\<Username>\Documents\Forensics`          | Manual (via tools)      | Placeholder for forensic disk image file.                                       |

## **Breakdown of Actions**

### **Files You Need to Populate Yourself**
- `Client_Reports.xlsx` (manual, placeholder).
- `Performance_Review.docx` (manual, placeholder).
- `Client_Transactions.xlsx` (manual, placeholder).
- `memory_dump.raw` (manual, forensic tool needed).
- `victim_disk_image.dd` (manual, forensic tool needed).

### **Files Automatically Created by Scripts**
- Log files (`network_traffic_log.txt`, `audit_log.txt`).
- Malware-related files (`encrypted_file_1.txt`, `.encryption_key`).
- PCAP files (`network_traffic.pcap`).
- Database (`Transactions_Backup.db`).

### **Files Modified by Scripts**
- `hosts` file (by `browser_simulation.py`).
- Event logs in `EventLog_Security.evtx` (by `log_manipulation.ps1`).


# Key Notes
- Kali VM is used for:
   - Monitoring network traffic using tshark or Wireshark.
   - Analyzing disk images and memory dumps.
   - Running forensic tools like Volatility, Sleuth Kit, and Plaso.

- Windows VM is used for:
   - Simulating the attack scenario by running all the attack scripts.
   - Generating artifacts such as logs, encrypted files, and phishing emails for forensic investigation.
   -Providing realistic evidence for analysis, including PCAP files and event logs.

