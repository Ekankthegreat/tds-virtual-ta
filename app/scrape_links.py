from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import json
import traceback

options = Options()
# options.add_argument("--headless")  # comment this to see browser open and watch what happens
options.add_argument("--disable-gpu")

driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
url = "https://tds.s-anand.net/#/2025-01/"
driver.get(url)

print("Page title:", driver.title)

try:
    print("Waiting for sidebar element...")
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "aside"))
    )
    print("Sidebar element found.")

    print("Executing JS to get links inside sidebar...")
    js_script = """
        let anchors = document.querySelectorAll('aside a');
        let urls = [];
        anchors.forEach(a => {
            if(a.href.includes('/#/')) {
                urls.push(a.href);
            }
        });
        return urls;
    """
    links = driver.execute_script(js_script)
    print(f"Number of links found: {len(links)}")
    
    if len(links) > 0:
        with open("tds_links.json", "w") as f:
            json.dump(links, f, indent=2)
        print("Links saved to tds_links.json")
    else:
        print("No links found inside sidebar.")

except Exception as e:
    print("Error occurred:")
    traceback.print_exc()

finally:
    driver.quit()
