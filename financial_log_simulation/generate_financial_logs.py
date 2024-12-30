import sqlite3
import random
from datetime import datetime, timedelta

def create_advanced_financial_logs():
    conn = sqlite3.connect('financial_logs.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS transactions 
                 (id INTEGER PRIMARY KEY, user TEXT, amount REAL, timestamp TEXT, ip TEXT, status TEXT, anomaly_flag TEXT)''')

    users = ['Dr. Wong', 'Michael Tan', 'Rachel Simmons']
    ips = ['192.168.1.105', '10.0.0.54', '203.0.113.25']
    statuses = ['Pending', 'Completed', 'Failed']
    anomaly_flags = ['None', 'Suspicious IP', 'Large Transfer', 'After-Hours Activity']

    for _ in range(1000):
        user = random.choice(users)
        amount = round(random.uniform(-20000, 50000), 2)
        timestamp = (datetime.now() - timedelta(seconds=random.randint(1, 86400))).strftime('%Y-%m-%d %H:%M:%S')
        ip = random.choice(ips)
        status = random.choice(statuses)

        # Flag anomalies
        anomaly = "None"
        if abs(amount) > 20000 or random.random() > 0.95:
            anomaly = random.choice(anomaly_flags)

        c.execute("INSERT INTO transactions (user, amount, timestamp, ip, status, anomaly_flag) VALUES (?, ?, ?, ?, ?, ?)", 
                  (user, amount, timestamp, ip, status, anomaly))

    conn.commit()
    conn.close()
    print("Advanced financial logs created successfully!")

if __name__ == "__main__":
    create_advanced_financial_logs()
