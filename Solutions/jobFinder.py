from bs4 import BeautifulSoup
import requests

htmlText = requests.get("https://www.remotepython.com/jobs/?q=Python")

soup = BeautifulSoup(htmlText.text, "html.parser")

counter = 1

allSections = soup.find_all(class_="item")
for section in allSections:
    print()
    print(f"----------Job {counter}----------")
    print(section.get_text().strip())
    print()
    counter += 1