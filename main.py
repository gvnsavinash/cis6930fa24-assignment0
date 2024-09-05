import argparse
import requests
import json
import sys

THORN = 'þ'

def fetch_data_from_api(page):
    """Fetch data from FBI API for the given page."""
    url = f"https://api.fbi.gov/wanted/v1/list?page={page}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        sys.exit(1)

def fetch_data_from_file(file_location):
    """Fetch data from a local JSON file."""
    try:
        with open(file_location, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"File not found: {file_location}")
        sys.exit(1)


def process_data(data):
    """Process and format the data to the required thorn-separated format."""
    output = []
    for item in data.get('items', []):
        # Safely retrieve title, subjects, and field offices
        title = item.get('title', 'N/A')
        
        # Handle subjects field
        subjects = ', '.join(item.get('subjects', [])) if isinstance(item.get('subjects', []), list) else 'N/A'
        
        # Handle field_offices field
        field_offices = item.get('field_offices', [])
        if not isinstance(field_offices, list):
            field_offices = []
        field_offices_str = ', '.join(field_offices)
        
        # Append the formatted data
        output.append(f"{title}{THORN}{subjects}{THORN}{field_offices_str}")
    
    return '\n'.join(output)

def main(page=None, file_location=None):
    """Main function to download data and print the thorn-separated file."""
    if page is not None:
        data = fetch_data_from_api(page)
    elif file_location is not None:
        data = fetch_data_from_file(file_location)
    else:
        print("Please specify either --page or --file-location")
        sys.exit(1)

    formatted_output = process_data(data)
    print(formatted_output)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="FBI Most Wanted List Data Fetcher")
    parser.add_argument("--page", type=int, required=False, help="Page number to fetch from the FBI API")
    parser.add_argument("--file-location", type=str, required=False, help="Location of the JSON file")

    args = parser.parse_args()

    if args.page:
        main(page=args.page)
    elif args.file_location:
        main(file_location=args.file_location)
    else:
        parser.print_help()
