import sys
import os.path

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
)
import main

def test_fetch_random_page():
    """Test fetching a random page from the FBI API."""
    import random
    random_page = random.randint(1, 5)
    data = main.fetch_fbi_wanted_list_by_page(random_page)
    
    assert isinstance(data, dict) and 'items' in data and data['items'], f"Invalid data for page {random_page}"

def test_invalid_page():
    """Test fetching data from an invalid page."""
    data = main.fetch_fbi_wanted_list_by_page(10000)
    assert 'items' in data and not data['items'], "Invalid page should return empty 'items'"

def test_random_page_special_characters():
    """Test handling of special characters in the random page response."""
    data = {"items": [{"title": "Test @Title$", "subjects": ["Subject!"], "field_offices": ["Office#"]}]}
    assert main.format_fbi_wanted_data(data) == "Test @Title$þSubject!þOffice#", "Special characters not handled correctly"

def test_random_page_with_empty_items():
    """Test handling of random page response where 'items' is empty."""
    data = {"items": []}
    assert main.format_fbi_wanted_data(data) == "", "Output should be empty for empty 'items'"