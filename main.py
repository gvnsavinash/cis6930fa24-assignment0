import argparse
import sys
import requests
import json

THORN = 'þ'

def fetch_fbi_wanted_list_by_page(page):
    """Fetch FBI wanted data from the API for the given page."""
    try:
        url = f"https://api.fbi.gov/wanted/v1/list?page={page}"
        response = requests.get(url)
        response.raise_for_status()  # Raises an exception for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from the API: {e}")
        sys.exit(1)

def load_json_from_file(file_location):
    """Load data from a JSON file."""
    try:
        with open(file_location, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"File not found: {file_location}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file: {file_location}")
        sys.exit(1)

def get_item_title(item):
    """Retrieve the title from the 'item' in the API data."""
    return item.get('title', '')

def get_item_subjects(item):
    """Retrieve and format the subjects from the 'item' in the API data."""
    subjects = item.get('subjects', [])
    if isinstance(subjects, list):
        return ', '.join(subjects)
    return ''

def get_item_field_offices(item):
    """Retrieve and organize the field offices from the 'item' in the API data."""
    field_offices = item.get('field_offices', [])
    if isinstance(field_offices, list):
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
        formatted_line = f"{title}{THORN}{subjects}{THORN}{field_offices}"
        formatted_lines.append(formatted_line)
    
    return '\n'.join(formatted_lines)

def main(page=None, file_location=None):
    """Download data and print the thorn-separated file."""
    if page is not None:
        data = fetch_fbi_wanted_list_by_page(page)
    elif file_location is not None:
        data = load_json_from_file(file_location)
    else:
        print("Please specify either --page or --file-location")
        sys.exit(1)

    formatted_output = format_fbi_wanted_data(data)
    print(formatted_output)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="API Data Retrieve: FBI Most Wanted List")
    parser.add_argument("--page", type=int, required=False, help="Include page number to fetch from the FBI API")
    parser.add_argument("--file-location", type=str, required=False, help="Include path location of the JSON file")

    args = parser.parse_args()

    if args.page:
        main(page=args.page)
    elif args.file_location:
        main(file_location=args.file_location)
    else:
        parser.print_help(sys.stderr)
