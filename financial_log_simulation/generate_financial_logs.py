"""
1. Creates a SQLite database with fake transactions involving Dr. Wong, Michael Tan, and Rachel Simmons.

2. Introduce Anomalies:
    - Suspicious transfers over $20,000 linked to Michael Tan.
    - Future timestamps to mimic log tampering.

3. Associates transactions with suspicious IPs to indicate unauthorized remote access.

Relation to the Attack Scenario:
    - Creates realistic financial logs reflecting the unauthorized $25,000 transfer from Dr. Wong's account.
    - Links suspicious transactions to Michael Tan and Rachel Simmons through IP addresses and anomalies.
    - Provides a rich source of evidence for investigators to analyze patterns and anomalies.
"""

import sqlite3
import random
from datetime import datetime, timedelta

def generate_financial_logs():
    conn = sqlite3.connect('financial_logs.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS transactions
                 (id INTEGER PRIMARY KEY, user TEXT, amount REAL, timestamp TEXT, ip TEXT, anomaly_flag TEXT)''')

    users = ["Dr. Wong", "Michael Tan", "Rachel Simmons"]
    ips = ["192.168.1.105", "10.0.0.54", "203.0.113.25"]
    anomaly_flags = ["None", "Suspicious Transfer", "After-Hours Access"]

    for _ in range(500):
        user = random.choice(users)
        amount = round(random.uniform(-20000, 50000), 2)
        timestamp = (datetime.now() - timedelta(seconds=random.randint(300, 86400))).strftime('%Y-%m-%d %H:%M:%S')
        ip = random.choice(ips)
        anomaly = "Suspicious Transfer" if user == "Michael Tan" and amount > 20000 else "None"

        # Introduce inconsistencies
        if random.random() < 0.1:
            timestamp = (datetime.now() + timedelta(hours=3)).strftime('%Y-%m-%d %H:%M:%S')  # Future timestamp

        c.execute("INSERT INTO transactions (user, amount, timestamp, ip, anomaly_flag) VALUES (?, ?, ?, ?, ?)",
                  (user, amount, timestamp, ip, anomaly))

    conn.commit()
    conn.close()
    print("[INFO] Financial logs created.")

if __name__ == "__main__":
    generate_financial_logs()
