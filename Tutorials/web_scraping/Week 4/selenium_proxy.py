import random
import requests

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# Get the list of proxies
url = "https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&proxy_format=ipport&format=text"
response = requests.get(url)
proxies_list = [proxy for proxy in response.text.split('\n') if proxy]

# Randomly select a proxy from the list
proxy = random.choice(proxies_list)

# Set up Chrome options with proxy and headless mode
options = Options()
#options.add_argument("--headless=new")
options.add_argument(f"--proxy-server=  https://{proxy}")
    
# Initialize the Chrome driver with service and Chrome options
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

try:
    # Visit target website
    driver.get(url)

    # Get the text area element
    text_area = driver.find_element(By.CLASS_NAME, "gLFyf")

    # Click on the search button
    search_button = driver.find_element(By.CLASS_NAME, "gNO89b")

    text_area.send_keys("College of DuPage")
    search_button.click()

finally:
    # Release the resources and close the browser
    driver.quit()
