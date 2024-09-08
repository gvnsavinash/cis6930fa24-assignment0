import sys
import os.path

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
)
import main

def test_fetch_random_page():
    """Test fetching a random page from the FBI API."""
    import random
    random_page = random.randint(1, 8)
    raw_data = main.fetch_fbi_wanted_list_by_page(random_page)
    
    assert isinstance(raw_data, dict) and 'items' in raw_data , f"Invalid data for page {random_page}"

def test_invalid_page():
    """Test fetching data from an invalid page."""
    raw_data = main.fetch_fbi_wanted_list_by_page(10000)
    assert 'items' in raw_data and not raw_data['items'], "Invalid page should return empty 'items'"


def test_get_item_title():
    """Test retrieving the title from an item in the API data."""
    item = {'title': 'Test_Title'}
    title = main.get_item_title(item)
    assert title == 'Test_Title', "Invalid title"