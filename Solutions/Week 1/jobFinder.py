import requests
from bs4 import BeautifulSoup
import pandas as pd

website = requests.get('https://www.remotepython.com/jobs/?q=Python').text
soup = BeautifulSoup(website, 'html.parser')

job_listings = soup.find_all(class_='col-md-11')
job_dict = {}

# Loops through each listing to gather job data
index = 1
for listing in job_listings:
    title = listing.find(class_='no-margin-top').text.strip()
    company = listing.find(class_='color-black').text
    description = listing.p.text.strip()
    posting_date = listing.div.find(class_='color-white-mute').text
    try:
        location = listing.h5.find(class_='color-white-mute').text
    except AttributeError:
        location = 'None given'

    # Updating dictionary with '{job title: {corresponding info}}'
    job_dict[f'job{index}'] = {'title': title, 'company': company, 'desc': description,
                               'date': posting_date, 'location': location}
    index += 1

    print(f'Title: {title}\nCompany: {company}\nDescription: {description}\n'
          f'Location: {location}\n{posting_date}\n')

print(job_dict)
df = pd.DataFrame(job_dict)
print(df)

