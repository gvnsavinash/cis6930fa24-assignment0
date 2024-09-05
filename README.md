# cis6930fa24 -- Assignment0

Name: Venkata Naga Satya Avinash, Gudipudi

---

## Project Description

This project is about working with the FBI’s Most Wanted API. We need to fetch data from the API and format it into a CSV-like structure with a special thorn character (`þ`) separating the values. The data includes information about people wanted by the FBI, such as the title, subjects, and field offices related to each case. 

You can either retrieve data directly from the FBI API or read it from a local JSON file.

---

## Implementation Steps

1. Data Retrieval: 
   - You can either fetch data from the FBI’s Most Wanted API or load it from a local JSON file.
   
2. Data Processing: 
   - The program extracts the title, subjects, and field offices for each record.
   
3. Formatting: 
   - The data is then formatted with a thorn character (`þ`) separating the values.

4. Output: 
   - The formatted data is printed to the console (standard output).

---

## Expected Output

The output is a list of records where each line follows this structure:

{title}þ{subjects}þ{field_offices}


For example, a sample output could look like this:

Extreme lossþsebastian,Pit BullþMiami
Dissapointing teamþDJþTallahassee,Dublin
Florida ManþSeeking InformationþGainesville
Data Engineerþþall over


---

## Environment Setup

To set up the environment, use `pipenv` to install the required packages. Run the following command in your project directory:


pipenv install 


This will create a virtual environment and install the dependencies needed to run the project.

---

## How to Run the Program

You can run the program in two ways:

1. Fetch data from the FBI API:

   Run the following command to retrieve data from a specific page of the FBI Most Wanted API:

   
   pipenv run python main.py --page <page_number>
   

   Replace `<page_number>` with a number like `1` or `2` to get the respective page from the API.

2. Load data from a local JSON file:

   If you want to load data from a local JSON file instead of the API, run the following command:

   
   pipenv run python main.py --file-location <path_to_json_file>
   

   Replace `<path_to_json_file>` with the actual path to your JSON file.
   In this Project FileName is "jsonfile.json"

---

## Functions

### `main.py` Functions

- `fetch_fbi_wanted_list_by_page(page)`: 

  - Fetches data from the FBI API for a specified page.
  
- `load_json_from_file(file_location)`: 

  - Loads data from a specified JSON file on your local machine.

- `get_item_title(item)`: 

  - Extracts the title from a record (e.g., the name of the wanted person or event).

- `get_item_subjects(item)`: 

  - Extracts and formats the subjects related to the case as a comma-separated list.

- `get_item_field_offices(item)`:

  - Extracts and formats the field offices handling the case as a comma-separated list.

- `format_fbi_wanted_data(data)`:

  - Formats the data into a thorn-separated format.

- `main(page=None, file_location=None)`: 

  - The main function that coordinates retrieving data (either from the API or a file), formatting it, and printing the output.

---

## Test Cases

There are two test files included in this project to ensure the functionality works as expected.

### `test_download.py`

This file includes the following tests:

1. `test_successful_data_download`:

   - Tests if data is successfully downloaded from the FBI API.
   
2. `test_empty_api_response`:

   - Checks how the program handles an empty API response.
   
3. `test_empty_strings_in_response`:

   - Ensures that empty fields in the API response are correctly handled (leaving them blank in the output).
   
4. `test_valid_data_structure`:

   - Verifies that the structure of the data is correct, containing the required fields (`title`, `subjects`, `field_offices`).
   
5. `test_duplicate_entries`:

   - Checks how the program handles duplicate entries in the API response.

6. `test_printing_thorn_separated_output`: 

   - Verifies if the formatted thorn-separated output is correctly printed for given test data.

### `test_randompage.py`

This file includes a test for retrieving data from a random page:

1. `test_fetch_random_page`:

   - Selects a random page number and verifies that data is fetched correctly from that page of the FBI API.

2. `test_invalid_page`: 

    - Ensures that fetching data from an invalid page returns an empty 'items' field.

3. `test_random_page_special_characters`:

    - Tests proper handling and formatting of special characters in the FBI wanted list data.

4. `test_random_page_with_empty_items`: 

    - Confirms that an empty 'items' field in the data returns an empty output.
   
---

## How to Run the Tests

To run the tests and verify that the program works as expected, use `pytest`:


pipenv run python -m pytest -v


The tests will automatically validate the main functionalities, such as downloading data and formatting it correctly.

---

## Bugs and Assumptions

Here’s a shortened version of the Bugs and Assumptions section:

---

## Bugs and Assumptions

1. API Structure Changes: If the API structure changes, the program may fail to process the data correctly.
2. Local JSON Format: The program expects the local JSON file to have the same structure as the API response.
3. Network Issues: No graceful handling of network timeouts or connection failures.
4. Command-Line Arguments: Either `--page` or `--file-location` must be provided. If neither or both are given, the program will exit with an error.
5. Special Characters: The program assumes the thorn (`þ`) character does not appear in the data fields.
6. Empty Fields: Empty or null fields are handled, but fully empty records might still appear in the output.
7. File Access: Assumes that the user has read permissions for the file in the `--file-location` option.
8. Data Consistency: The program expects the data to be consistently formatted. Inconsistent entries may cause issues.
---
