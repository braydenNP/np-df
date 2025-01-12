import os
import sqlite3
import json
from datetime import datetime, timedelta
import random

# Updated directory structure
directory_structure = {
    os.path.expanduser(r"~\Documents\FinancialData"): [
        "Transactions_Backup.db",  # Populated
        "Client_Reports.xlsx",  # Blank
        "Performance_Review.docx"  # Blank
    ],
    os.path.expanduser(r"~\Documents\Work_Reports"): [
        "summary.txt",  # Populated
        "log_analysis_report.txt",  # Populated
        "encrypted_file_1.txt",  # Populated
        "encrypted_file_2.txt",  # Populated
    ],
    os.path.expanduser(r"~\AppData\Local\Microsoft\Outlook"): [
        "internal_review.eml",  # Populated
        "q3_analysis_report.eml"  # Populated
    ],
    os.path.expanduser(r"~\AppData\Local\Google\Chrome\User Data\Default"): [
        "History",  # Populated by browser_simulation.py
        "Cache"  # Populated by browser_simulation.py
    ],
    r"C:\Windows\System32\drivers\etc": [
        "hosts"  # Modified in browser_simulation.py
    ]
}

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"[INFO] Created directory: {path}")
    else:
        print(f"[INFO] Directory exists: {path}")

def create_file(path):
    if path.endswith(".db"):
        populate_database(path)
    elif path.endswith(".eml"):
        populate_email(path)
    elif path.endswith(".txt"):
        populate_text_file(path)
    else:
        open(path, 'a').close()
        print(f"[INFO] Created blank file: {path}")

def populate_database(path):
    if not os.path.exists(path):
        conn = sqlite3.connect(path)
        c = conn.cursor()
        c.execute('''CREATE TABLE transactions
                     (id INTEGER PRIMARY KEY, user TEXT, amount REAL, timestamp TEXT, ip TEXT, anomaly_flag TEXT)''')
        for _ in range(100):
            user = random.choice(["Dr. Wong", "Michael Tan", "Rachel Simmons"])
            amount = round(random.uniform(-20000, 50000), 2)
            timestamp = (datetime.now() - timedelta(seconds=random.randint(300, 86400))).strftime('%Y-%m-%d %H:%M:%S')
            ip = random.choice(["192.168.1.105", "10.0.0.54", "203.0.113.25"])
            anomaly_flag = "Suspicious Transfer" if user == "Michael Tan" else "None"
            c.execute("INSERT INTO transactions (user, amount, timestamp, ip, anomaly_flag) VALUES (?, ?, ?, ?, ?)",
                      (user, amount, timestamp, ip, anomaly_flag))
        conn.commit()
        conn.close()
        print(f"[INFO] Populated database: {path}")

def populate_email(path):
    if not os.path.exists(path):
        with open(path, "w") as f:
            f.write(f"From: Rachel Simmons <rachel@company.com>\n")
            f.write(f"To: Michael Tan <michael@company.com>\n")
            f.write("Subject: Q3 Review\n")
            f.write("Body: Please find the Q3 analysis attached. Ensure you review it by EOD.\n")
        print(f"[INFO] Populated email: {path}")

def populate_text_file(path):
    if not os.path.exists(path):
        with open(path, "w") as f:
            for i in range(10):
                f.write(f"Entry {i + 1}: This is a dummy log entry.\n")
        print(f"[INFO] Populated text file: {path}")

def main():
    for directory, files in directory_structure.items():
        create_directory(directory)
        for file in files:
            create_file(os.path.join(directory, file))

if __name__ == "__main__":
    main()