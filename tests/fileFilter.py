import pytest
from twinTrim.dataStructures.fileFilter import FileFilter

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
