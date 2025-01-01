import subprocess
import os
from datetime import datetime
import time

LOG_FILE = "execution_log.txt"

def log_message(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as log_file:
        log_file.write(f"[{timestamp}] {message}\n")

def run_script(script_path, script_type="python"):
    try:
        log_message(f"START: {script_path}")
        if script_type == "python":
            subprocess.run(["python", script_path], check=True)
        elif script_type == "powershell":
            subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", script_path], check=True)
        log_message(f"SUCCESS: {script_path}")
    except subprocess.CalledProcessError as e:
        log_message(f"ERROR: {script_path} - {e}")
    except Exception as e:
        log_message(f"CRITICAL ERROR: {script_path} - {e}")

if __name__ == "__main__":
    scripts = [
        {"path": "scripts/browser_activity/browser_simulation.py", "type": "python"},
        {"path": "scripts/email_simulation/email_generator.py", "type": "python"},
        {"path": "scripts/financial_logs/generate_financial_logs.py", "type": "python"},
        {"path": "scripts/log_manipulation/event_log_generator.ps1", "type": "powershell"},
        {"path": "scripts/malware_simulation/malware_simulator.py", "type": "python"},
        {"path": "scripts/network_traffic/network_traffic_generator.py", "type": "python"},
    ]

    log_message("=== Script Execution Started ===")
    for script in scripts:
        run_script(script["path"], script["type"])
        time.sleep(5)  # Mimic real-world delay
    log_message("=== Script Execution Finished ===")
