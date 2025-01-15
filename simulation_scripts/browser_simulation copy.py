from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import os
import json
from datetime import datetime


def manipulate_dns():
    """Simulate DNS cache poisoning by logging the event (no actual file modification)."""
    print("[INFO] Simulating DNS cache poisoning for banking-related traffic.")



def simulate_browsing_activity():
    """Simulate realistic browsing activity with hidden artifacts."""
    sites = [
        {"url": "https://www.wikipedia.org", "search_terms": ["financial fraud", "cryptocurrency"]},
        {"url": "https://www.duckduckgo.com", "search_terms": ["anonymous transactions", "crypto wallet setup"]},
        {"url": "https://www.reddit.com", "search_terms": ["money laundering techniques", "secure transactions"]},
    ]

    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36",
    ]

    options = Options()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(f"user-agent={random.choice(user_agents)}")
    driver = webdriver.Chrome(options=options)

    for i in range(3):
        try:
            if (i == 0):
                #Wikipedia
                driver.get("https://www.wikipedia.org")
                print(f"[INFO] Browsing wikipedia.org")

                # Wait for the page to load fully
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )

                # Simulate adding cookies
                driver.add_cookie({"name": "session", "value": f"{random.randint(1000, 9999)}", "path": "/"})

                # Try searching for terms if a search box is available
                try:
                    search_term = "financial fraud"
                    driver.get(f"https://en.wikipedia.org/wiki/Special:Search?go=Go&search={search_term}&ns0=1")
                    time.sleep(random.uniform(2, 4))
                    search_term = "cryptocurrency3"
                    driver.get(f"https://en.wikipedia.org/wiki/Special:Search?go=Go&search={search_term}&ns0=1")
                    time.sleep(random.uniform(2, 4))
                except Exception:
                    print(f"[WARNING] wikipedia search failed")
            if (i == 1):
                #Duckduckgo
                driver.get("https://duckduckgo.com/")
                print(f"[INFO] Browsing duckduckgo.com")

                # Wait for the page to load fully
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )

                # Simulate adding cookies
                driver.add_cookie({"name": "session", "value": f"{random.randint(1000, 9999)}", "path": "/"})

                # Try searching for terms if a search box is available
                try:
                    search_term = "anonymous transactions"
                    driver.get(f"https://duckduckgo.com/?t=h_&q={search_term}")
                    time.sleep(random.uniform(2, 4))
                    search_term = "crypto wallet setup"
                    driver.get(f"https://duckduckgo.com/?t=h_&q={search_term}")
                    time.sleep(random.uniform(2, 4))
                except Exception:
                    print(f"[WARNING] duckduckgo search failed")
            if (i == 2):
                #Duckduckgo
                driver.get("https://www.reddit.com")
                print(f"[INFO] Browsing reddit.com")

                # Wait for the page to load fully
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )

                # Simulate adding cookies
                driver.add_cookie({"name": "session", "value": f"{random.randint(1000, 9999)}", "path": "/"})

                # Try searching for terms if a search box is available
                try:
                    search_term = "money laundering techniques"
                    driver.get(f"https://www.reddit.com/search/?q={search_term}")
                    time.sleep(random.uniform(2, 4))
                    search_term = "secure transactions"
                    driver.get(f"https://www.reddit.com/search/?q={search_term}")
                    time.sleep(random.uniform(2, 4))
                except Exception:
                    print(f"[WARNING] reddit search failed")

            # Interact with links on the page
            links = driver.find_elements(By.TAG_NAME, "a")
            for link in links[:3]:  # Interact with up to 3 links
                href = link.get_attribute("href")
                if href:
                    print(f"[INFO] Visiting link: {href}")
                    driver.get(href)
                    WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.TAG_NAME, "body"))
                    )
                    time.sleep(random.uniform(2, 5))

            # Simulate creating temporary files (e.g., fake malware artifacts)
            download_dir = f"C:\\Users\\{os.getlogin()}\\Downloads"
            os.makedirs(download_dir, exist_ok=True)
            temp_file = os.path.join(download_dir, f"{random.randint(1000, 9999)}.tmp")
            with open(temp_file, "w") as f:
                f.write(json.dumps({"content": "Temporary session data...", "timestamp": datetime.now().isoformat()}))
            print(f"[INFO] Temporary file created: {temp_file}")

        except Exception as e:
            print(f"[ERROR] Error during browsing: {e}")

    driver.quit()


if __name__ == "__main__":
    manipulate_dns()
    simulate_browsing_activity()
