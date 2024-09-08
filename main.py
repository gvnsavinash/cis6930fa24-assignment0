import argparse
import sys
import requests
import json
# import csv

THORN = 'þ'

def fetch_fbi_wanted_list_by_page(page):
    """Fetch FBI wanted data from the API for the given page."""
    try:
        url = f"https://api.fbi.gov/wanted/v1/list?page={page}"
        response = requests.get(url)
        response.raise_for_status()  # Raises an exception for bad responses
        return response.json()
    except Exception as e:
        print(f"Expection Error : {e}")
        sys.exit(1)

def load_json_from_file(file):
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
    """Retrieve and format the subjects from the 'item' in the API data."""
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
        data = fetch_fbi_wanted_list_by_page(page)
    elif thefile is not None:
        data = load_json_from_file(thefile)
    else:
        print("Please specify either --page or --file-location")
        sys.exit(1)

    formatted_output = format_fbi_wanted_data(data)

    # Print to standard output with thorn separator
    for item in formatted_output:
        print(f"{item['title']}{THORN}{item['subjects']}{THORN}{item['field_offices']}")

    # Save to CSV file
    #save_to_csv(formatted_output)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="API Data Retrieve: FBI Most Wanted List")
    parser.add_argument("--page", type=int, required=False, help="Include page number to fetch from the FBI API")
    parser.add_argument("--file", type=str, required=False, help="Include path location of the JSON file")
    
    args = parser.parse_args()

    if args.page:
        main(page=args.page)
    elif args.file:
        main(thefile=args.file)
    else:
        parser.print_help(sys.stderr)
