import pandas as pd
import requests
from bs4 import BeautifulSoup

def main():

    #makes sure the data is displayed in its entirety
    pd.set_option("display.max_rows", None)


    url = "https://en.wikipedia.org/wiki/2024_Summer_Olympics_medal_table"
    data = pd.read_html(url)

    #Stores the right index for the medal table in an appropriate variable
    medalTable = data[3]

    #Adds spacing to the beginning and end so that data is more readable
    print("\n")
    print("\n")

    #Gets rid of the index column
    print(medalTable.to_string(index=False))
    print("\n")
    print("\n")



main()