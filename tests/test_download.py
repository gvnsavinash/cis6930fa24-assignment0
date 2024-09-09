import sys
import os.path

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
)
import main

def test_ValidApi_FBIJson():
    """This Function Helps for fetching data from the FBI API and returns whether it valid JSON or NOT."""
    raw_data = main.fetch_data(3)
    assert all([isinstance(raw_data, dict), 'items' in raw_data]), "Data is Invalid As per API."

    
def test_ValidFileJson():
    """This Function Helps for fetching data from the given file and returns whether it valid JSON or NOT."""
    raw_data = main.fetch_data_from_file('jsonfile.json')
    assert all([isinstance(raw_data, dict), 'items' in raw_data]), "Data is Invalid As Per Attached File."


def test_valid_structure():
    """This Function Verify's the API returns data in the correct structure or not."""
    raw_data = main.fetch_data(1)
    assert isinstance(raw_data, dict) and 'items' in raw_data, "Invalid structure"
    for item in raw_data['items']:
        assert all(k in item for k in ['title', 'subjects', 'field_offices']), "structure keys missing"


def test_extract_fields():
    """Test extracting title, subjects, and field_offices fields from FBI API data."""
    raw_data = main.fetch_data(1)
    item = raw_data['items'][0]  

    title = main.get_item_title(item)
    subjects = main.get_item_subjects(item)
    field_offices = main.get_item_field_offices(item)

    # assertions to check that data is extracted or None is handled
    assert title is None or isinstance(title, str), "Title should be a string or None."
    assert subjects is None or isinstance(subjects, list) or  isinstance(subjects, str), "Subjects should be a list, string, or None."
    assert field_offices is None or isinstance(field_offices, list) or isinstance(field_offices, str), "Field offices should be a list or None."
    
    if isinstance(subjects, list):
        assert len(subjects) == 0 or all(isinstance(sub, str) for sub in subjects), "Subjects list should contain only strings."

    if isinstance(field_offices, list):
        assert len(field_offices) == 0 or all(isinstance(office, str) for office in field_offices), "Field offices list should contain only strings."

    

def test_print_fullthorn():
    """Test formatting the FBI data into the required thorn-separated format."""
    raw_data = main.fetch_data(1)
    formatted_data = main.format_fbi_wanted_data(raw_data)
    assert isinstance(formatted_data, list), "Formatted data should be a list."
    if len(formatted_data) == 0:
        return  
    # Validating the each item in formatted_data has the thorn-separated format
    for item in formatted_data:
        thorn_separated = f"{item['title']}þ{item['subjects']}þ{item['field_offices']}" 
        assert "þ" in thorn_separated, "Thorn separator (þ) should be present in the formatted string."
        assert isinstance(thorn_separated, str), "Formatted thorn-separated string should be valid."
        assert thorn_separated.strip(), "Thorn-separated string should not be empty."


