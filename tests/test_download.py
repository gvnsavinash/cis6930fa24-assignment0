import sys
import os

# Add the parent directory of `tests` to sys.path so that `main.py` can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import main

def test_fetch_data_from_api():
    """Test that fetching data from the FBI API returns valid JSON."""
    page = 1  # Test the first page
    data = main.fetch_data_from_api(page)
    
    assert isinstance(data, dict), "API response should be a dictionary."
    assert 'items' in data, "API response should contain 'items'."
    assert len(data['items']) > 0, "API response 'items' should not be empty."

def test_process_data():
    """Test processing the data from the API."""
    # Simulated API response data
    data = {
        "items": [
            {"title": "Test Title", "subjects": ["Subject1", "Subject2"], "field_offices": ["office1", "office2"]}
        ]
    }
    
    result = main.process_data(data)
    assert result == "Test TitleþSubject1, Subject2þoffice1, office2", "Processed data does not match expected output."
