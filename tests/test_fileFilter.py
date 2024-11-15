import pytest
from twinTrim.dataStructures.fileFilter import FileFilter


# Test setting valid max file size values
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

# Test setting the same max file size
def test_set_max_file_size_same_value():
    """Test setting the same max file size value multiple times."""
    file_filter = FileFilter()

    # Test setting the max file size to the default value
    file_filter.setMaxFileSize("1gb")
    assert file_filter.maxFileSize == "1gb", "Failed to set max file size to 1gb"

    # Test setting the max file size to the same value again
    file_filter.setMaxFileSize("1gb")
    assert file_filter.maxFileSize == "1gb", "Failed to set max file size to 1gb again"

# Test boundary values for max file size
def test_set_max_file_size_boundary():
    """Test boundary values for max file size."""
    file_filter = FileFilter()

    # Test setting a value just under the default
    file_filter.setMaxFileSize("999mb")
    assert file_filter.maxFileSize == "999mb", "Failed to set max file size to 999mb"

    # Test setting a value just over the default
    file_filter.setMaxFileSize("1001mb")
    assert file_filter.maxFileSize == "1001mb", "Failed to set max file size to 1001mb"

# Test setting an empty value to max file size
def test_set_max_file_size_empty_value():
    """Test setting an empty value to max file size."""
    file_filter = FileFilter()

    # Since there is no validation, an empty value would still set it to the empty string
    file_filter.setMaxFileSize("")
    assert file_filter.maxFileSize == "", "Failed to set max file size to empty value"

# Test adding files to the exclude list
def test_add_file_exclude_adds_file():
    """Test adding a file to the exclude list."""
    file_filter = FileFilter()
    file_filter.addFileExclude("test_file.txt")
    assert "test_file.txt" in file_filter.fileExclude, "File was not added to the exclude list"


# Test setting valid file types
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

# Test setting an empty string as file type
def test_set_file_type_empty_string():
    """Test setting an empty string as file type."""
    file_filter = FileFilter()

    # The empty string should be accepted and form a regex matching any file without an extension
    file_filter.setFileType("")
    assert file_filter.fileType == r"^.+\.$", "Failed to set file type regex for empty file type"

# Test setting file types with special characters
def test_set_file_type_special_characters():
    """Test setting file types with special characters."""
    file_filter = FileFilter()

    # Special characters should be part of the file extension in the regex
    file_filter.setFileType("mp4#")
    assert file_filter.fileType == r"^.+\.mp4#$", "Failed to set file type regex for special characters"

# Test setting numeric file type extensions
def test_set_file_type_numeric():
    """Test setting numeric file type extensions."""
    file_filter = FileFilter()

    # File types with numbers should be accepted
    file_filter.setFileType("123")
    assert file_filter.fileType == r"^.+\.123$", "Failed to set file type regex for numeric file type"
