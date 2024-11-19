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
import time
import random
import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium_stealth import stealth
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebElement
from selenium.webdriver.chrome.webdriver import WebDriver as ChromeDriver
from selenium.common import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
# Exceptions to ignore when waiting for
# element searching to return a value
ignored_exceptions = (NoSuchElementException, StaleElementReferenceException)

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
    titles = driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="searchSerpJob"]')
    
    for title in titles:
        title.click()
        job_dict['UNIQUE_TITLE'].append("SoftDev")
        jobtitle = title.find_element(By.TAG_NAME,"a" )
        job_dict['TITLE'].append(jobtitle.text.strip())
        location = title.find_element(By.CLASS_NAME, "css-1t92pv")
        job_dict['JOB_LOCATION'].append(location.text.strip())
        company_name = title.find_element(By.CSS_SELECTOR, 'span[data-testid="companyName"]')
        job_dict['COMPANY_NAME'].append(company_name.text.strip())
        driver.implicitly_wait(5)
        try:
            job_type = driver.find_element(By.CSS_SELECTOR, 'span[data-testid="viewJobBodyJobDetailsJobType"]').find_element(By.CSS_SELECTOR, 'span[data-testid="detailText"]' )
            job_dict['JOB_TYPE'].append(job_type.text.strip())
        except Exception as err:
            job_dict['JOB_TYPE'].append("unknown")

        try:
            salary_wage = driver.find_element(By.CSS_SELECTOR, 'span[data-testid="viewJobBodyJobCompensation"]').find_element(By.CSS_SELECTOR, 'span[data-testid="detailText"]')
            job_dict['SALARY'].append(salary_wage.text.strip())
        except Exception as err:
            job_dict['SALARY'].append("unknown")

        try:
            qual_list = []
            all_quals = driver.find_elements(By.CSS_SELECTOR, 'span[data-testid="viewJobQualificationItem"]')
            for qual in all_quals:
                qual_list.append(qual.text.strip())
            job_dict['QUALIFICATIONS'].append(qual_list)
        except Exception as err:
            print("not found")

def next_page(driver: ChromeDriver):
       
    try:
        driver.implicitly_wait(random.uniform(0.5, 0.9))
        next_page_button = driver.find_element(By.CLASS_NAME, "css-1puj5o8")
        next_page_button.click()
        time.sleep(4)
        #print('in next page')
        
    except NoSuchElementException:
        print("Next Page structure misalignment!")
    except StaleElementReferenceException:
        print("Element no longer detected: next page operations")

def scroll_down(driver):
    while True:
        last_height = driver.execute_script("return document.body.scrollHeight")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

        driver.implicitly_wait(5)  # Wait 5 seconds

        # Get the new height and compare with last height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            scrape_page()
            break
        last_height = new_height


def main():
    # Set up Chrome options
    chrome_options = Options()
    # Choose a random User-Agent from the list
    random_user_agent = random.choice(user_agents)
    chrome_options.add_argument(f"--user-agent={random_user_agent}")

    #driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    driver = webdriver.Chrome(options=chrome_options)

    job_dict = {"UNIQUE_TITLE":[],          # Unique job title
                "TITLE": [],                # Title of the job
                "JOB_LOCATION": [],         # Location ( State )
                "COMPANY_NAME": [],         # Company name
                "JOB_TYPE": [],             # Whether full-time, part-time, intern
                #"remote": [],               # Remote, in-person, hybrid
                #"wage": [],                 # $ per hour
                "SALARY": [],               # $ per year
                #"education": [],            # Undergrad, master, phd
                #"prog_language": [],        # Programming languages
                #"framework": [],            # React, Angular, Django, Flask, etc
                "QUALIFICATIONS":[]          # Database, Cloud technologies, etc
                }

    url = "https://www.simplyhired.com/search?q=software+developer&l=Chicago%2C+IL"
    # Visit target website
    driver.get(url)

    

    for i in range(1):
        scrape_page(driver, job_dict)
        next_page(driver)
        
            
    driver.quit()

    df = pd.DataFrame(job_dict)
    print(df)


if __name__ == '__main__':
    main()