import subprocess
import random
from datetime import datetime
import time

LOG_FILE = "simulation_log.txt"

def log_message(message):
    """Log a message with a timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as log:
        log.write(f"[{timestamp}] {message}\n")

def execute_script(script_path, script_type="python"):
    """Execute a script and log the result."""
    try:
        log_message(f"Starting {script_path}")
        if script_type == "python":
            subprocess.run(["python", script_path], check=True)
        elif script_type == "powershell":
            subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", script_path], check=True)
        log_message(f"Completed {script_path}")
    except subprocess.CalledProcessError as e:
        log_message(f"Error in {script_path}: {e}")
    except Exception as e:
        log_message(f"Critical error in {script_path}: {e}")

def setup_environment():
    """Call create_dir.py to set up directories and files."""
    try:
        log_message("Starting create_dir.py")
        subprocess.run(["python", "create_dir.py"], check=True)
        log_message("create_dir.py completed successfully.")
    except subprocess.CalledProcessError as e:
        log_message(f"Error in create_dir.py: {e}")
    except Exception as e:
        log_message(f"Critical error in create_dir.py: {e}")

if __name__ == "__main__":
    # Step 1: Set up directories and files
    setup_environment()

    # Step 2: Execute the rest of the scripts
    scripts = [
        {"path": "browser_simulation.py", "type": "python"},
        {"path": "email_simulation.py", "type": "python"},
        {"path": "financial_logs.py", "type": "python"},
        {"path": "log_manipulation.ps1", "type": "powershell"},
        {"path": "malware_simulation.py", "type": "python"},
    ]

    log_message("Simulation started.")
    for script in scripts:
        execute_script(script["path"], script["type"])
        delay = random.randint(300, 900)  # Realistic delay (5-15 minutes)
        log_message(f"Waiting {delay} seconds before next script.")
        time.sleep(delay)
    log_message("Simulation completed.")
