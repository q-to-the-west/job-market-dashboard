import pandas as pd
import requests
from bs4 import BeautifulSoup


# Fetch and parse the website HTML
def extract_html(website):
    try:
        response = requests.get(website)
        response.raise_for_status()  # Raises an error for bad status codes
        return BeautifulSoup(response.text, 'html.parser')
    except requests.RequestException as e:
        print(f"Error fetching the website: {e}")
        return None

# Extract job details and return as a DataFrame
def find_jobs(soup):
    if not soup:
        return pd.DataFrame()  # Return empty DataFrame if soup is None

    jobs = []

    job_cards = soup.find_all("div", class_="col-md-11")

    for job in job_cards:
        jobs.append({
            'Title': job.find(class_="no-margin-top").get_text().strip(),
            'Company': job.find(class_="color-black").get_text().strip(),
            'Location': job.find("span", class_="color-white-mute").get_text().strip(),
            'Description': job.find("p").get_text().strip()
        })
    return pd.DataFrame(jobs)


def main():
    url = "https://www.remotepython.com/jobs/?q=Python"
    soup = extract_html(url)

    jobs = find_jobs(soup)
    if not jobs.empty:
        print(jobs.iloc[0])


if __name__ == "__main__":
    main()
