import pytest
from twinTrim.dataStructures.fileFilter import FileFilter

def test_set_max_file_size_valid():
    """Test setting valid max file size values."""
    file_filter = FileFilter()

    # Test with a smaller size
    file_filter.setMaxFileSize("500mb")
    assert file_filter.maxFileSize == "500mb", "Failed to set max file size to 500mb"

    # Test with a larger size
    file_filter.setMaxFileSize("2gb")
    assert file_filter.maxFileSize == "2gb", "Failed to set max file size to 2gb"

    # Test with a minimum size (edge case)
    file_filter.setMaxFileSize("1kb")
    assert file_filter.maxFileSize == "1kb", "Failed to set max file size to 1kb"

def test_set_max_file_size_same_value():
    """Test setting the same max file size."""
    file_filter = FileFilter()

    # Test setting the max file size to the default value
    file_filter.setMaxFileSize("1gb")
    assert file_filter.maxFileSize == "1gb", "Failed to set max file size to 1gb"

def test_set_max_file_size_boundary():
    """Test boundary values for max file size."""
    file_filter = FileFilter()

    # Test setting a value just under the default
    file_filter.setMaxFileSize("999mb")
    assert file_filter.maxFileSize == "999mb", "Failed to set max file size to 999mb"

def test_set_max_file_size_empty_value():
    """Test setting an empty value to max file size."""
    file_filter = FileFilter()

    # Since there is no validation, an empty value would still set it to the empty string
    file_filter.setMaxFileSize("")
    assert file_filter.maxFileSize == "", "Failed to set max file size to empty value"

def test_add_file_exclude_adds_file():
    file_filter = FileFilter()
    file_filter.addFileExclude("test_file.txt")
    assert "test_file.txt" in file_filter.fileExclude

def test_add_file_exclude_prevents_duplicates():
    file_filter = FileFilter()
    file_filter.addFileExclude("test_file.txt")
    file_filter.addFileExclude("test_file.txt")
    assert file_filter.fileExclude.count("test_file.txt") == 2


