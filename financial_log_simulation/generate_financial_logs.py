import sqlite3
import random
from datetime import datetime, timedelta

def generate_financial_logs():
    """Generate realistic financial transaction logs."""
    db_name = "financial_logs.db"
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    # Create transactions and audit tables
    c.execute('''CREATE TABLE IF NOT EXISTS transactions
                 (id INTEGER PRIMARY KEY, user TEXT, amount REAL, timestamp TEXT, ip TEXT, anomaly_flag TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS audit_log
                 (id INTEGER PRIMARY KEY, action TEXT, timestamp TEXT, user TEXT, details TEXT)''')

    users = ["Dr. Wong", "Michael Tan", "Rachel Simmons", "Susan Lee"]
    ips = ["192.168.1.105", "10.0.0.54", "203.0.113.25", "198.51.100.14"]
    anomaly_flags = ["None", "Suspicious Transfer", "After-Hours Access", "Inconsistent Data"]

    # Generate financial transactions
    for _ in range(500):
        user = random.choice(users)
        amount = round(random.uniform(-20000, 50000), 2)
        timestamp = (datetime.now() - timedelta(seconds=random.randint(300, 86400))).strftime('%Y-%m-%d %H:%M:%S')
        ip = random.choice(ips)
        anomaly = random.choice(anomaly_flags) if user == "Michael Tan" else "None"

        # Introduce inconsistencies in timestamp
        if random.random() < 0.05:
            timestamp = (datetime.now() + timedelta(hours=random.randint(1, 3))).strftime('%Y-%m-%d %H:%M:%S')

        c.execute("INSERT INTO transactions (user, amount, timestamp, ip, anomaly_flag) VALUES (?, ?, ?, ?, ?)",
                  (user, amount, timestamp, ip, anomaly))

        # Log suspicious activities in the audit log
        if anomaly != "None":
            action = "Suspicious Transaction"
            details = f"User {user} performed {anomaly} from IP {ip}."
            c.execute("INSERT INTO audit_log (action, timestamp, user, details) VALUES (?, ?, ?, ?)",
                      (action, timestamp, user, details))

    conn.commit()
    conn.close()
    print(f"[INFO] Financial logs and audit log generated in {db_name}")

if __name__ == "__main__":
    generate_financial_logs()