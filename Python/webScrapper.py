import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

# URL of the site to scrape
url = "https://www.bbc.com/news"

# Step 1: Send an HTTP request
response = requests.get(url, verify=False)

# Step 2: Parse the HTML content
soup = BeautifulSoup(response.content, 'html.parser')

pattern = re.compile(r'\b(sc-.*-3)\b')

# Step 3: Extract unique data
unique_headlines = set()  # Use a set to store unique headlines
for item in soup.find_all('h2', attrs={'class': pattern}):
    headline = item.text.strip()  # Strip any extra whitespace
    if headline not in unique_headlines:  # Check if it's not already added
        unique_headlines.add(headline)  # Add to the set

headlines_list = list(unique_headlines)

# Step 4: Save the data
df = pd.DataFrame({'Headline': headlines_list})
df.to_csv('headlines.csv', index=False)

print("Headlines saved to 'headlines.csv'")
