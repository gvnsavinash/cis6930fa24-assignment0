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
    assert isinstance(data, dict) and 'items' in data and data['items'], "Invalid data"

def test_empty_api_response():
    """Check how an empty API response is handled."""
    assert main.format_fbi_wanted_data({"items": []}) == "", "Not empty"

def test_empty_strings_in_response():
    """Check if empty strings in API response fields are handled properly."""
    data = {"items": [{"title": "", "subjects": [""], "field_offices": [""]}]}
    assert main.format_fbi_wanted_data(data) == "þþ", "Invalid empty string handling"

def test_valid_data_structure():
    """Verify that the API returns data in the correct structure."""
    data = main.fetch_fbi_wanted_list_by_page(1)
    assert isinstance(data, dict) and 'items' in data, "Invalid structure"
    for item in data['items']:
        assert all(k in item for k in ['title', 'subjects', 'field_offices']), "Missing keys"

def test_duplicate_entries():
    """Check how duplicate items in the API response are handled."""
    data = {"items": [{"title": "Duplicate Title", "subjects": ["Subject A"], "field_offices": ["Office X"]}] * 2}
    assert main.format_fbi_wanted_data(data).count("Duplicate Title") == 2, "Duplicates not handled"

def test_printing_thorn_separated_output():
    """Test if the formatted thorn-separated output is printed correctly."""
    test_data = {
        "items": [
            {"title": "Test Title", "subjects": ["Test Subject"], "field_offices": ["Test Office"]},
            {"title": "Another Title", "subjects": ["Another Subject"], "field_offices": ["Another Office"]}
        ]
    }  
    expected_output = "Test TitleþTest SubjectþTest Office\nAnother TitleþAnother SubjectþAnother Office\n"
    captured_output = StringIO()
    sys.stdout = captured_output
    # Format and print the data
    main.format_fbi_wanted_data(test_data)
    print(main.format_fbi_wanted_data(test_data))
    sys.stdout = sys.__stdout__
    # Assert the captured output matches the expected output
    assert captured_output.getvalue() == expected_output, "Output does not match expected thorn-separated format"