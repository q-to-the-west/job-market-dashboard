import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_website(url):
    response = requests.get(url)
    return response.text

def parse_html(html):
        soup = BeautifulSoup(html, "html.parser")

        # Dictionary to hold all the information
        country_info = {
            "Country":[],
            "Capital":[],
            "Population":[],
            "Area (km^2)":[]
        }

        # Each country information ar stored in this class
        items = soup.find_all(class_="col-md-4 country")

        # Loop to get the country, capita, population, area of each item and store in the dictionary
        for item in items:
            country = item.find(class_="country-name").get_text().strip()
            capital = item.find(class_="country-capital").get_text().strip()
            population = item.find(class_="country-population").get_text().strip()
            area = item.find(class_="country-area" ).get_text().strip()

            country_info["Country"].append(country)
            country_info["Capital"].append(capital)
            country_info["Population"].append(population)
            country_info["Area (km^2)"].append(area)

        # Transform the dictionary into a dataframe
        df = pd.DataFrame(country_info)
        return df

def df_analysis(dataframe):

    # Check the dataframe out
    print("\n", dataframe.info())

    # The Population and Area are string, so we need to convert them to integers
    dataframe["Population"] = dataframe["Population"].astype(int)

    # https://pandas.pydata.org/docs/reference/api/pandas.to_numeric.html#pandas.to_numeric
    # Downcast = cast to numerical dtype
    # errors="coerce" = If it can't be casted, change it to "NaN"
    dataframe["Area (km^2)"] = pd.to_numeric(dataframe["Area (km^2)"], downcast="integer", errors="coerce")
    print("\n", dataframe.info())

    # Getting the country with the highest population
    largest_pop = dataframe["Population"].idxmax()
    print("\nCountry with the highest population:\n", dataframe.iloc[largest_pop])

    # Getting the country with the highest total area
    largest_area = dataframe["Area (km^2)"].idxmax()
    print("\nCountry with the largest area:\n", dataframe.iloc[largest_area])

    # The top 5 largest country
    largest_country = dataframe.sort_values(by=["Area (km^2)"], ascending=False)
    print("\nLargest countries:\n", largest_country.head())

    # Top 5 countries with the most population
    largest_population = dataframe.sort_values(by=["Population"], ascending=False)
    print("\nLargest population:\n", largest_population.head())

    # Total population
    total_pop = dataframe["Population"].sum()
    print(f"\nTotal population: {total_pop:,} people")

    # Total land area
    total_area = dataframe["Area (km^2)"].sum()
    print(f"\nTotal area:\n{total_area:,} km^2")

    # Descriptive analysis of the dataframe
    print("\n", dataframe.describe())


def main():
    url = "https://www.scrapethissite.com/pages/simple/"

    html_text = get_website(url)
    soup = parse_html(html_text)

    # Visualize the top 5 entries of the dataframe
    print(soup.head())
    print()
    # Visualize the last 5 entries of the dataframe
    print(soup.tail())
    print()

    df_analysis(soup)


if __name__ == "__main__":
    main()
