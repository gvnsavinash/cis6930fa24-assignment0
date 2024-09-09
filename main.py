import argparse
import sys
import urllib.request
import requests
import json
import random
# import csv

THORN = 'þ'

def fetch_data(page):
    """
    Fetches data from the FBI API.
    Parameters:
    - page (int): The page number of the data to fetch.
    Returns:
    - dict: The JSON data fetched from the API.
    Raises:
    - Exception: If an error occurs while fetching the data.
    """
    url = f"https://api.fbi.gov/wanted/v1/list?page={page}"
    
    # randomized User-Agent string by selecting from different components
    platforms = ["X11; Linux x86_64", "Windows NT 10.0; Win64; x64", "Macintosh; Intel Mac OS X 10_15_7"]
    browsers = ["Chrome/90.0.4430.212", "Firefox/89.0", "Safari/537.36"]
    user_agent = f"Mozilla/5.0 ({random.choice(platforms)}) AppleWebKit/537.36 (KHTML, like Gecko) {random.choice(browsers)}"

    headers = {
        'User-Agent': user_agent
    }
    try:
        request = urllib.request.Request(url, headers=headers)
        # Fetch the data from the API
        with urllib.request.urlopen(request) as response:
            return json.load(response)
    except Exception as e:
        print(f"Error occurred while fetching data: {e}")
        sys.exit(1)

def fetch_data_from_file(file):
    """Load data from a JSON file."""
    try:
        with open(file, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"Expection Error : {e}")
        sys.exit(1)

def get_item_title(item):
    """Retrieve the title from the 'item' in the API data."""
    return item.get('title', '')

def get_item_subjects(item):
    """
    Returns a string representation of the subjects associated with the given item.
    Parameters:
    - item (dict): A dictionary representing an item.
    Returns:
    - str: A string representation of the subjects, separated by commas. If no subjects are found, an empty string is returned.
    """
    subjects = item.get('subjects', [])
    if isinstance(subjects, list):
        #print("sub",subjects)
        return ', '.join(subjects)
    return ''

def get_item_field_offices(item):
    """Retrieve and organize the field offices from the 'item' in the API data."""
    field_offices = item.get('field_offices', [])
    if isinstance(field_offices, list):
        #print("field",field_offices)
        return ', '.join(field_offices)
    return ''

def format_fbi_wanted_data(data):
    """Process and organize the data into the required thorn-separated format."""
    if not isinstance(data, dict) or 'items' not in data:
        print("Invalid data structure.")
        sys.exit(1)
    
    formatted_lines = []
    for item in data.get('items', []):
        title = get_item_title(item)
        subjects = get_item_subjects(item)
        field_offices = get_item_field_offices(item)
        
        # Filter based on the search term if provided
        formatted_lines.append({
            'title': title,
            'subjects': subjects,
            'field_offices': field_offices
        })
    
    return formatted_lines

# def save_to_csv(data, file='output.csv'):
#     """Save the formatted data to a CSV file with proper columns."""
#     with open(file, 'w', newline='', encoding='utf-8') as csvfile:
#         csv_writer = csv.DictWriter(csvfile, fieldnames=['title', 'subjects', 'field_offices'])
#         csv_writer.writeheader()
#         csv_writer.writerows(data)

def main(page=None, thefile=None, search_term=None):
    """Download data and print the thorn-separated file."""
    if page is not None:
        data = fetch_data(page)
    elif thefile is not None:
        data = fetch_data_from_file(thefile)
    else:
        print("Please specify either --page or --file-location")
        sys.exit(1)

    formatted_output = format_fbi_wanted_data(data)

    for item in formatted_output:
        print(f"{item['title']}{THORN}{item['subjects']}{THORN}{item['field_offices']}")

    # Save to CSV file
    #save_to_csv(formatted_output)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="API Data Retrieve: FBI Most Wanted List")
    parser.add_argument("--file", type=str, required=False, help="Include path location of the JSON file")
    parser.add_argument("--page", type=int, required=False, help="Include page number to fetch from the FBI API")
    
    
    args = parser.parse_args()

    if args.page:
        main(page=args.page)
    elif args.file:
        main(thefile=args.file)
    else:
        parser.print_help(sys.stderr)
