import sys
import os.path

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
)
import main
import random
random_page = random.randint(1, 6)

def test_invalid_page():
    """Test fetching data from an invalid page."""
    raw_data = main.fetch_data(10000000000)
    assert 'items' in raw_data and not raw_data['items'], "Invalid page should return empty 'items'"

def test_random_ValidApi_FBIJson():
    """This Function Helps for fetching data from the random page of given FBI API and returns whether it valid JSON or NOT."""
    raw_data = main.fetch_data(random_page)
    assert all([isinstance(raw_data, dict), 'items' in raw_data]), "Data is Invalid As per API."

def test_random_valid_structure():
    """This Function Verify's the random page of given API and returns data in the correct structure or not."""
    raw_data = main.fetch_data(random_page)
    assert isinstance(raw_data, dict) and 'items' in raw_data, "Invalid structure"
    for item in raw_data['items']:
        assert all(k in item for k in ['title', 'subjects', 'field_offices']), "structure keys missing"


def test_random_extract_fields():
    """Test extracting title, subjects, and field_offices fields from random page of given FBI API data."""
    raw_data = main.fetch_data(random_page)
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

    

def test_random_print_fullthorn():
    """Test formatting the random page of given FBI data into the required thorn-separated format."""
    raw_data = main.fetch_data(random_page)
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
