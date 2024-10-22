import selenium.webdriver as webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd

def scrape_page(driver, podcast_episodes):
    posts = driver.find_elements(By.CLASS_NAME, "post")

    for post in posts:
        title = post.find_element(By.CLASS_NAME, "post__title").text.strip()
        released_date, duration = post.find_element(By.CLASS_NAME, "post__date").text.split("|")
        link = post.find_element(By.CLASS_NAME, "button-light").text.strip()  # .get_attribute("href")

        podcast_episodes["Title"].append(title)
        podcast_episodes["Released"].append(released_date.strip())
        podcast_episodes["Duration"].append(duration.strip())
        podcast_episodes["Link"].append(link)

def navigate_to_next_page(driver):
    try:
        next_page_button = driver.find_element(By.LINK_TEXT, "Older Episodes")
        next_page_button.click()
        return True
    except NoSuchElementException:
        return False

def main():
    print("Launching Chrome browser...")
    url = "https://darknetdiaries.com/episode/"
    chrome_driver_path = "../../../Testing/chromedriver.exe"

    # Create a dictionary to hold the values
    podcast_episodes = {"Title": [], "Released": [], "Duration": [], "Link": []}

    # Set up driver
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument("--headless=new")

    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=chrome_options)
    driver.implicitly_wait(10)  # Wait 10 seconds

    # Visit target website
    driver.get(url)

    # Scrape all pages
    while True:
        scrape_page(driver, podcast_episodes)
        if not navigate_to_next_page(driver):
            print("No more pages to scrape.")
            break

    driver.quit()
    df = pd.DataFrame(podcast_episodes)
    print(df)

if __name__ == "__main__":
    main()
