import requests
from bs4 import BeautifulSoup
import csv
import datetime
import argparse

def fetch_data(url, selectors):
    # Send a GET request to the URL
    response = requests.get(url)

    # Error handling
    if response.status_code == 200:
        print("Successfully fetched the webpage!")
    else:
        print(f"Error: Failed to fetch webpage. Status code: {response.status_code}")
        exit(1)

    # Parse the HTML content of the webpage
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract data based on user-provided selectors
    data = {}
    for selector in selectors:
        data[selector] = [item.text.strip() for item in soup.select(selector)]
    
    return data

def save_data_to_csv(data):
    # Generate a unique filename with timestamp
    now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  # Current date and time
    filename = f"scraped_data_{now}.csv"

    # Open the CSV file for writing in write mode
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=data.keys())
        
        writer.writeheader()

        # Write each data as a row
        for i in range(len(data[list(data.keys())[0]])):
            row = {key: data[key][i] for key in data.keys()}
            writer.writerow(row)

    print(f"Extracted data saved to {filename}")

def main():
    parser = argparse.ArgumentParser(description='Web Scraping Application')
    parser.add_argument('--url', type=str, help='URL of the website to scrape')
    parser.add_argument('--selectors', nargs='+', help='Selectors for data extraction')
    args = parser.parse_args()

    if args.url is None:
        url = input("Enter the URL of the website to scrape(example:http://quotes.toscrape.com/): ")
    else:
        url = args.url

    if args.selectors is None:
        selectors_input = input("Enter the selectors for data extraction (separated by space)(example:.author .text): ") #.author and .text are the classes of the data to scrape
        selectors = selectors_input.split()
    else:
        selectors = args.selectors

    data = fetch_data(url, selectors)
    save_data_to_csv(data)

if __name__ == "__main__":
    main()
