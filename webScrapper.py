import requests
from bs4 import BeautifulSoup
import time
import json
import re

# retry mechanism na data scrapping function
def fetch_data_with_retries(url, retries=3, delay=2):
    """Fetch data from a URL with Retry a request if it fails."""
    for attempt in range(retries):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad responses
            return response.text
        except requests.RequestException as e:
            print(f"Attempt: {attempt + 1} failed with error: {e}")
            if attempt < retries - 1:
                time.sleep(delay * (attempt + 1))  # Exponential backoff
            else:
                raise
   
# Function to extract data using BeautifulSoup4 and regular expressions
def extract_data_from_html(html_content):
    """Extract data from HTML content using BeautifulSoup."""
    if not html_content:
        raise ValueError("Html content is invalid or empty")
    
    soup = BeautifulSoup(html_content, 'html.parser')
    titles =[]
    
    #Regular expression to find all the links with the specific text(python)
    for link in soup.find_all('a', href=True):
        title =link.get_text()
        if re.match(r'.*python.*', title, re.IGNORECASE):  #looking for links containing the word python
            titles.append(title)
    
    return titles

# Function to save data to a JSON file
def save_data_to_json(data, filename):
    """Save data to a JSON file."""
    if not data:
        raise ValueError("Data is empty or invalid")
    try:
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"Data saved to {filename}")
    
    except Exception as e:
        print(f"Error saving data to JSON: {e}")

# URL to scrape
url = "https://www.python.org/"

# Fetch, extract, and save data

html_content = fetch_data_with_retries(url)
extracted_data = extract_data_from_html(html_content)
save_data_to_json(extracted_data, 'extracted_data.json')