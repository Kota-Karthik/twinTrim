import pytest
from twinTrim.dataStructures.fileFilter import FileFilter


def test_set_min_file_size_valid():
    """Test setting valid minimum file size values."""
    file_filter = FileFilter()

    # Test with a larger valid size
    file_filter.setMinFileSize("20kb")
    assert file_filter.minFileSize == "20kb", "Failed to set min file size to 20kb"

    # Test with a smaller valid size
    file_filter.setMinFileSize("5kb")
    assert file_filter.minFileSize == "5kb", "Failed to set min file size to 5kb"

    # Test with an edge case (1kb)
    file_filter.setMinFileSize("1kb")
    assert file_filter.minFileSize == "1kb", "Failed to set min file size to 1kb"

def test_set_min_file_size_empty_string():
    """Test setting an empty string for minimum file size."""
    file_filter = FileFilter()

    # Empty string should be allowed since no validation exists
    file_filter.setMinFileSize("")
    assert file_filter.minFileSize == "", "Failed to set min file size to an empty string"

def test_set_min_file_size_special_characters():
    """Test setting special characters or random string as min file size."""
    file_filter = FileFilter()

    # Special characters should be accepted since no validation exists
    file_filter.setMinFileSize("!!invalid!!")
    assert file_filter.minFileSize == "!!invalid!!", "Failed to set min file size to special characters"

def test_set_min_file_size_numeric_string():
    """Test setting numeric string as minimum file size."""
    file_filter = FileFilter()

    # Numeric string should be accepted, even without units
    file_filter.setMinFileSize("123")
    assert file_filter.minFileSize == "123", "Failed to set min file size to a numeric string"

