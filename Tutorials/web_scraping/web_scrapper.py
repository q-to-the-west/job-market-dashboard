from bs4 import BeautifulSoup
import requests

# Fetch the HTML text and transform it in text
html_text = requests.get("https://docs.python-guide.org/writing/style/#zen-of-python").text

# Parse the HTML
soup = BeautifulSoup(html_text, 'html.parser')

# Try to find the 'zen_of_python' section by its id
zen_code = soup.find(id="zen-of-python")

# Display the text
print(zen_code.get_text())

