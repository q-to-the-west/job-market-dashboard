import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


chrome_driver_path = "../../../Testing/chromedriver.exe"
user_input = input("Search for: ")
url = "https://www.google.com.br/"

# Set up driver
chrome_options = webdriver.ChromeOptions()

# Headless browser
#chrome_options.add_argument("--headless=new")
driver = webdriver.Chrome(service=Service(chrome_driver_path), options=chrome_options)
driver.implicitly_wait(10)  # Wait 10 seconds

# Visit target website
driver.get(url)

# Get the text area element
text_area = driver.find_element(By.CLASS_NAME, "gLFyf")

# Click on the search button
search_button = driver.find_element(By.CLASS_NAME, "gNO89b")

text_area.send_keys(user_input)
search_button.click()