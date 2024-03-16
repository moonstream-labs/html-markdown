import requests
from bs4 import BeautifulSoup

# Prompt the user for the URL input
url = input("Please enter the URL to fetch and prettify HTML: ")

try:
    # Fetch the content from the URL using requests
    response = requests.get(url)
    
    # Ensure the request was successful
    response.raise_for_status()
    
    # Use Beautiful Soup to parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Prettify the parsed HTML
    prettified_html = soup.prettify()
    
    # Print the prettified HTML
    print(prettified_html)
except requests.RequestException as e:
    # Handle potential errors (e.g., network issues, invalid URL)
    print(f"An error occurred: {e}")
