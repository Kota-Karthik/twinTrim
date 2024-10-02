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

def test_set_file_type_valid():
    """Test setting valid file types."""
    file_filter = FileFilter()

    # Test setting a common file type
    file_filter.setFileType("txt")
    assert file_filter.fileType == r"^.+\.txt$", "Failed to set file type regex for .txt files"

    # Test setting a file type with multiple extensions
    file_filter.setFileType("tar.gz")
    assert file_filter.fileType == r"^.+\.tar.gz$", "Failed to set file type regex for .tar.gz files"

    # Test setting a single character file type
    file_filter.setFileType("c")
    assert file_filter.fileType == r"^.+\.c$", "Failed to set file type regex for .c files"

def test_set_file_type_empty_string():
    """Test setting an empty string as file type."""
    file_filter = FileFilter()

    # The empty string should be accepted and form a regex matching any file without an extension
    file_filter.setFileType("")
    assert file_filter.fileType == r"^.+\.$", "Failed to set file type regex for empty file type"

def test_set_file_type_special_characters():
    """Test setting file types with special characters."""
    file_filter = FileFilter()

    # Special characters should be part of the file extension in the regex
    file_filter.setFileType("mp4#")
    assert file_filter.fileType == r"^.+\.mp4#$", "Failed to set file type regex for special characters"

def test_set_file_type_numeric():
    """Test setting numeric file type extensions."""
    file_filter = FileFilter()

    # File types with numbers should be accepted
    file_filter.setFileType("123")
    assert file_filter.fileType == r"^.+\.123$", "Failed to set file type regex for numeric file type"

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


