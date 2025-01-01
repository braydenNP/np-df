from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import random
import os
from datetime import datetime

def manipulate_dns():
    """Simulate DNS cache poisoning by redirecting bank traffic."""
    with open("C:\\Windows\\System32\\drivers\\etc\\hosts", "a") as f:
        f.write("203.0.113.25 www.fakebank.com\n")
    print("[INFO] DNS cache manipulated to redirect bank traffic.")

def simulate_browsing_activity():
    """Simulate realistic browsing activity with hidden artifacts."""
    sites = [
        {"url": "https://www.fakebank.com", "search_terms": ["transfer $25,000 to crypto wallet", "disable fraud detection"]},
        {"url": "https://www.cryptowallet.com", "search_terms": ["create anonymous wallet", "send BTC"]},
        {"url": "https://darkwebforum.com", "search_terms": ["laundering money", "secure transactions"]}
    ]

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0")
    driver = webdriver.Chrome(options=options)

    for site in sites:
        driver.get(site["url"])
        print(f"[INFO] Browsing {site['url']}")
        time.sleep(random.uniform(2, 5))

        try:
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
            temp_file = f"C:\\Temp\\{random.randint(1000,9999)}.tmp"
            with open(temp_file, "w") as f:
                f.write("Temporary session data...")
            print(f"[INFO] Temporary file created: {temp_file}")
        except Exception as e:
            print(f"[ERROR] Error during browsing: {e}")

    # Delete temporary files to simulate attacker cleanup
    for temp_file in os.listdir("C:\\Temp"):
        try:
            os.remove(f"C:\\Temp\\{temp_file}")
            print(f"[INFO] Temporary file deleted: {temp_file}")
        except Exception as e:
            print(f"[ERROR] Failed to delete temporary file: {e}")

    driver.quit()

if __name__ == "__main__":
    manipulate_dns()
    simulate_browsing_activity()
