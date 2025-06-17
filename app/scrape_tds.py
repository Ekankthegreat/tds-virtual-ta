# app/scrape_tds.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import json
import time

def scrape_tds_site():
    url = "https://tds.s-anand.net"

    options = Options()
    options.add_argument("--headless=new")  # headless for faster scraping
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)

        # Wait for the left sidebar to appear
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".MenuItems"))
        )

        # Expand all sections
        expand_buttons = driver.find_elements(By.CSS_SELECTOR, ".MenuItems .menu-icon")
        for btn in expand_buttons:
            try:
                btn.click()
                time.sleep(0.3)
            except:
                continue

        # Now collect all content pages
        links = driver.find_elements(By.CSS_SELECTOR, ".MenuItems a")

        content_blocks = []

        for link in links:
            href = link.get_attribute("href")
            if not href:
                continue
            driver.get(href)

            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "main"))
                )
                time.sleep(1)  # give extra time for JS to load content

                title = driver.title.strip()
                body = driver.find_element(By.CSS_SELECTOR, "main").text.strip()

                if len(body) > 20:
                    content_blocks.append(f"{title}\n{body}")

            except Exception as e:
                print(f"⚠️ Failed to load: {href}")

        with open("app/data/tds_content.json", "w", encoding="utf-8") as f:
            json.dump(content_blocks, f, indent=2, ensure_ascii=False)

        print(f"✅ Saved {len(content_blocks)} content blocks to app/data/tds_content.json")

    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_tds_site()
