"""
    This template file contains a few functions to help with web scraping
        * scrape_page()
            This function's purpose is to scrape a webpage as the name suggests
        * next_page()
            This function's purpose is to click on an element to move to the next page
        * scroll_down()
            This function handle webpages that needs to scroll down to load new content
        * main()
            You can find here the main the dataframe we are using for this project
"""

import random
import pandas as pd
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium_stealth import stealth
from selenium.webdriver.support import expected_conditions as EC




# List of user agents string
user_agents = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
               "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
               "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.2420.81",
               "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0",
               "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
               "Mozilla/5.0 (Macintosh; Intel Mac OS X 14.4; rv:124.0) Gecko/20100101 Firefox/124.0",
               "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15",
               "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0",
               "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
               "Mozilla/5.0 (X11; Linux i686; rv:124.0) Gecko/20100101 Firefox/124.0"]


def scrape_page(driver, job_dict):

    job_cards = driver.find_elements(By.CSS_SELECTOR, "div.job_result_two_pane")


    for job in job_cards:
        title = job.find_element(By.CSS_SELECTOR, "h2.font-bold.text-black.text-header-sm").text
        company = job.find_element(By.CSS_SELECTOR, "p > a[data-testid='job-card-company']").text
        location = job.find_element(By.CSS_SELECTOR, "p > a[data-testid='job-card-location']").text

        job_dict["title"].append(title)
        job_dict["job_location"].append(location)
        job_dict["company_name"].append(company)
        #job_dict["salary"].append(salary)
        #job_dict["job_type"].append(job_type)




def next_page(driver):
    try:
        next_page_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "css-1vk6oae")))
        next_page_button.click()
        return True
    except NoSuchElementException:
        print("No more pages available")
        return False

def main():
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument("start-maximized")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    # run in headless mode
    chrome_options.add_argument("--headless")

    # disable the AutomationControlled feature of Blink rendering engine
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')

    # disable pop-up blocking
    chrome_options.add_argument('--disable-popup-blocking')

    # start the browser window in maximized mode
    chrome_options.add_argument('--start-maximized')

    # disable extensions
    chrome_options.add_argument('--disable-extensions')

    # disable sandbox mode
    chrome_options.add_argument('--no-sandbox')

    # disable shared memory usage
    chrome_options.add_argument('--disable-dev-shm-usage')

    # Choose a random User-Agent from the list
    random_user_agent = random.choice(user_agents)
    chrome_options.add_argument(f"--user-agent={random_user_agent}")

    # create a driver instance
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

    # Change the property value of the navigator for webdriver to undefined
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")


    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )

    job_dict = {#"unique_title":[],          # Unique job title
                "title": [],                # Title of the job
                "job_location": [],         # Location ( State )
                "company_name": [],         # Company name
                #"job_type": [],             # Whether full-time, part-time, intern
                #"remote": [],               # Remote, in-person, hybrid
                #"wage": [],                 # $ per hour
                #"salary": [],               # $ per year
                #"education": [],            # Undergrad, master, phd
                #"prog_language": [],        # Programming languages
                #"framework": [],            # React, Angular, Django, Flask, etc
                #"others":[]                 # Database, Cloud technologies, etc
                }

    url = "https://www.ziprecruiter.com/jobs-search?search=software+engineer&location=Chicago%2C+IL&lvk=JG_74EGAdtycohHKniD2eg.--NacsUqfMF"

    # Visit target website
    driver.get(url)
    scrape_page(driver, job_dict)

    df = pd.DataFrame(job_dict)
    print(df)
    print(df.describe)
    print(df.info)
    print(df.iloc[0])

if __name__ == '__main__':
    main()