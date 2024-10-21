import pandas as pd
import requests
from bs4 import BeautifulSoup

# URL of the page containing the table
url = 'https://en.wikipedia.org/wiki/2024_Summer_Olympics_medal_table'

# Get the page content
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Find the specific table by class
table = soup.find('table', class_='wikitable')

# Initialize an empty dictionary to store the data
medal_table = {
    'Rank': [],
    'Country': [],
    'Gold': [],
    'Silver': [],
    'Bronze': [],
    'Total': []
}

# Loop through the rows of the table
for row in table.find_all('tr')[1:]:  # Skipping the header row
    columns = row.find_all(['th', 'td'])  # Use both <th> and <td> to get all data

    # Check if the row has enough columns (6 columns for Rank, NOC, Gold, Silver, Bronze, Total)
    if len(columns) >= 6:
        rank = columns[0].get_text(strip=True)
        noc = columns[1].get_text(strip=True)
        gold = columns[2].get_text(strip=True)
        silver = columns[3].get_text(strip=True)
        bronze = columns[4].get_text(strip=True)
        total = columns[5].get_text(strip=True)

        # Append the data to the corresponding list in the dictionary
        medal_table['Rank'].append(rank)
        medal_table['Country'].append(noc)
        medal_table['Gold'].append(gold)
        medal_table['Silver'].append(silver)
        medal_table['Bronze'].append(bronze)
        medal_table['Total'].append(total)

# Create a DataFrame from the dictionary
df = pd.DataFrame(medal_table)

# Display the DataFrame
print(df.head())
