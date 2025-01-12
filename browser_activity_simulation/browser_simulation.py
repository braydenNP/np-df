from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import random
import os
import json
from datetime import datetime

def manipulate_dns():
    """Simulate DNS cache poisoning by redirecting bank traffic."""
    try:
        with open("C:\\Windows\\System32\\drivers\\etc\\hosts", "a") as f:
            f.write("203.0.113.25 www.fakebank.com\n")
        print("[INFO] DNS cache manipulated to redirect bank traffic.")
    except PermissionError:
        print("[ERROR] Permission denied: Unable to modify hosts file.")

def simulate_browsing_activity():
    """Simulate realistic browsing activity with hidden artifacts."""
    sites = [
        {"url": "https://www.fakebank.com", "search_terms": ["transfer $25,000 to crypto wallet", "disable fraud detection"]},
        {"url": "https://www.cryptowallet.com", "search_terms": ["create anonymous wallet", "send BTC"]},
        {"url": "https://darkwebforum.com", "search_terms": ["laundering money", "secure transactions"]},
    ]

    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36",
    ]

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(f"user-agent={random.choice(user_agents)}")
    driver = webdriver.Chrome(options=options)

    for site in sites:
        try:
            driver.get(site["url"])
            print(f"[INFO] Browsing {site['url']}")

            # Simulate adding cookies
            driver.add_cookie({"name": "session", "value": f"{random.randint(1000, 9999)}", "path": "/"})

            time.sleep(random.uniform(2, 5))

            # Simulate searching
            search_box = driver.find_element(By.NAME, "q")
            search_term = random.choice(site["search_terms"])
            search_box.send_keys(search_term + Keys.RETURN)
            time.sleep(random.uniform(2, 4))

            # Interact with links
            links = driver.find_elements(By.TAG_NAME, "a")
            for link in links[:3]:
                print(f"[INFO] Visiting link: {link.get_attribute('href')}")
                link.click()
                time.sleep(random.uniform(2, 5))

            # Create temporary files (simulating downloaded malware)
            download_dir = f"C:\\Users\\{os.getlogin()}\\Downloads"
            os.makedirs(download_dir, exist_ok=True)
            temp_file = os.path.join(download_dir, f"{random.randint(1000, 9999)}.tmp")
            with open(temp_file, "w") as f:
                f.write(json.dumps({"content": "Temporary session data...", "timestamp": datetime.now().isoformat()}))
            print(f"[INFO] Temporary file created: {temp_file}")

        except Exception as e:
            print(f"[ERROR] Error during browsing {site['url']}: {e}")

    driver.quit()

if __name__ == "__main__":
    manipulate_dns()
    simulate_browsing_activity()