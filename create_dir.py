import os
import sqlite3
import json
from datetime import datetime, timedelta
import random

# Define directory and file structure
directory_structure = {
    "C:\\FinancialData": [
        "Transaction_Logs_Backup.db",  # Populated
        "Client_Transactions.xlsx",   # Blank (manually populated)
        "Quarterly_Report.docx"       # Blank (manually populated)
    ],
    "C:\\Temp\\Encrypted_Files": [
        "file_1.txt", "file_2.txt", "file_3.txt"  # Populated
    ],
    "C:\\Users\\MichaelTan\\AppData\\Local\\.hidden_wallets": [
        "wallet.dat", "transaction_log.txt"  # Populated
    ],
    "C:\\Users\\MichaelTan\\AppData\\Local\\.unauthorized_exports": [
        "Dr_Wong_Transactions.csv", "Client_Data_Dump.sql"  # Populated
    ]
}

# Helper functions
def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"[INFO] Directory created: {path}")
    else:
        print(f"[INFO] Directory already exists: {path}")

def create_or_populate_file(path):
    if path.endswith(".db"):
        populate_database(path)
    elif path.endswith(".txt"):
        populate_text_file(path)
    elif path.endswith(".csv"):
        populate_csv_file(path)
    elif path.endswith(".sql"):
        populate_sql_file(path)
    elif path.endswith(".dat"):
        populate_wallet_file(path)
    else:
        create_blank_file(path)

def create_blank_file(path):
    if not os.path.exists(path):
        with open(path, "w") as f:
            pass
        print(f"[INFO] Blank file created: {path}")
    else:
        print(f"[INFO] File already exists: {path}")

# File population functions
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
        print(f"[INFO] Database populated: {path}")

def populate_text_file(path):
    if not os.path.exists(path):
        with open(path, "w") as f:
            for i in range(20):  # Dummy lines
                f.write(f"Line {i + 1}: This is dummy content.\n")
        print(f"[INFO] Text file populated: {path}")

def populate_csv_file(path):
    if not os.path.exists(path):
        with open(path, "w") as f:
            f.write("TransactionID,User,Amount,Date,IP\n")
            for i in range(1, 101):  # 100 dummy rows
                user = random.choice(["Dr. Wong", "Michael Tan", "Rachel Simmons"])
                amount = round(random.uniform(100, 25000), 2)
                date = (datetime.now() - timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d')
                ip = random.choice(["192.168.1.105", "10.0.0.54", "203.0.113.25"])
                f.write(f"{i},{user},{amount},{date},{ip}\n")
        print(f"[INFO] CSV file populated: {path}")

def populate_sql_file(path):
    if not os.path.exists(path):
        with open(path, "w") as f:
            f.write("CREATE TABLE exports (id INTEGER PRIMARY KEY, data TEXT);\n")
            for i in range(50):  # 50 rows
                f.write(f"INSERT INTO exports (id, data) VALUES ({i}, 'Exported Data {i}');\n")
        print(f"[INFO] SQL file populated: {path}")

def populate_wallet_file(path):
    if not os.path.exists(path):
        wallet_data = {
            "wallet_id": "abc123",
            "balance": 50000,
            "transactions": [
                {"id": 1, "amount": -5000, "date": "2024-01-01"},
                {"id": 2, "amount": 15000, "date": "2024-01-05"}
            ]
        }
        with open(path, "w") as f:
            f.write(json.dumps(wallet_data, indent=4))
        print(f"[INFO] Wallet file populated: {path}")

# Main function
def main():
    for directory, files in directory_structure.items():
        create_directory(directory)
        for file in files:
            file_path = os.path.join(directory, file)
            create_or_populate_file(file_path)

if __name__ == "__main__":
    main()