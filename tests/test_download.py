import sys
import os.path
from io import StringIO

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
)
import main

def test_successful_data_download():
    """Check if fetching data from the FBI API returns valid JSON."""
    data = main.fetch_fbi_wanted_list_by_page(1)
    assert isinstance(data, dict) and 'items' in data , "Invalid data"



def test_valid_data_structure():
    """Verify that the API returns data in the correct structure."""
    data = main.fetch_fbi_wanted_list_by_page(1)
    assert isinstance(data, dict) and 'items' in data, "Invalid structure"
    for item in data['items']:
        assert all(k in item for k in ['title', 'subjects', 'field_offices']), "Missing keys"


def test_load_json_from_file():
    """Test loading data from a JSON file."""
    data = main.load_json_from_file('jsonfile.json')
    assert isinstance(data, dict) and 'items' in data, "Invalid data structure"