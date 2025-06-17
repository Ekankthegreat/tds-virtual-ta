from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

# Step 1: Setup headless Chrome
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')

# Step 2: Let webdriver-manager install the matching ChromeDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Step 3: Visit the TDS course site
url = 'https://tds.s-anand.net/#/2025-01/'
driver.get(url)

# Step 4: Wait for the page to load
time.sleep(5)

# Step 5: Print page title to check it works
print("Page title:", driver.title)

driver.quit()
