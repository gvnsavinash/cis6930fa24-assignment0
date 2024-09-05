import sys
import os

# Add the parent directory of `tests` to sys.path so that `main.py` can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import main

def test_fetch_random_page():
    """Test fetching a random page from the FBI API."""
    import random
    random_page = random.randint(1, 5)  # Random page number between 1 and 5 for testing

    data = main.fetch_data_from_api(random_page)
    
    assert isinstance(data, dict), "API response should be a dictionary."
    assert 'items' in data, "API response should contain 'items'."
    assert len(data['items']) > 0, f"API response 'items' for page {random_page} should not be empty."

def test_invalid_page():
    """Test fetching data from an invalid page."""
    invalid_page = 10000  # Use an invalid page number to test error handling
    data = main.fetch_data_from_api(invalid_page)
    
    assert 'items' in data, "API response should contain 'items'."
    assert len(data['items']) == 0, "Invalid page should return an empty 'items' list."
