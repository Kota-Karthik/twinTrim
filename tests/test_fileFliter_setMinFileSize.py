import pytest
from twinTrim.dataStructures.fileFilter import FileFilter

def test_set_min_file_size_valid():
    """Test setting valid min file size values."""
    file_filter = FileFilter()
    
    # Test with a smaller size
    file_filter.setMinFileSize("10kb")
    assert file_filter.minFileSize == "10kb", "Failed to set min file size to 10kb"
    
    # Test with a larger size
    file_filter.setMinFileSize("500mb")
    assert file_filter.minFileSize == "500mb", "Failed to set min file size to 500mb"
    
    # Test with a minimum size (edge case)
    file_filter.setMinFileSize("1b")
    assert file_filter.minFileSize == "1b", "Failed to set min file size to 1b"

def test_set_min_file_size_same_value():
    """Test setting the same min file size."""
    file_filter = FileFilter()
    
    # Assuming the default min file size is 0b
    file_filter.setMinFileSize("0b")
    assert file_filter.minFileSize == "0b", "Failed to set min file size to 0b"

def test_set_min_file_size_boundary():
    """Test boundary values for min file size."""
    file_filter = FileFilter()
    
    # Test setting a value just above the assumed default
    file_filter.setMinFileSize("1b")
    assert file_filter.minFileSize == "1b", "Failed to set min file size to 1b"

def test_set_min_file_size_empty_value():
    """Test setting an empty value to min file size."""
    file_filter = FileFilter()
    
    # Since there is no validation, an empty value would still set it to the empty string
    file_filter.setMinFileSize("")
    assert file_filter.minFileSize == "", "Failed to set min file size to empty value"

def test_set_min_file_size_zero():
    """Test setting zero as the min file size."""
    file_filter = FileFilter()
    
    file_filter.setMinFileSize("0b")
    assert file_filter.minFileSize == "0b", "Failed to set min file size to 0b"

def test_set_min_file_size_different_units():
    """Test setting min file size with different units."""
    file_filter = FileFilter()
    
    file_filter.setMinFileSize("1mb")
    assert file_filter.minFileSize == "1mb", "Failed to set min file size to 1mb"
    
    file_filter.setMinFileSize("1024kb")
    assert file_filter.minFileSize == "1024kb", "Failed to set min file size to 1024kb"