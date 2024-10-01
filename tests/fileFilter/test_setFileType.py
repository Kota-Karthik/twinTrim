import re
import pytest
from  twinTrim.dataStructures.fileFilter import FileFilter
import sys
import os



@pytest.fixture
def file_filter():
    return FileFilter()

def test_set_file_type_with_valid_extension(file_filter):
    # Test with valid file extensions
    file_filter.setFileType("txt")
    assert re.match(file_filter.fileType, "example.txt")
    assert not re.match(file_filter.fileType, "example.pdf")

    file_filter.setFileType("pdf")
    assert re.match(file_filter.fileType, "example.pdf")
    assert not re.match(file_filter.fileType, "example.txt")

def test_set_file_type_with_multiple_extensions(file_filter):
    # Test with multiple valid extensions
    file_filter.setFileType("(txt|pdf)")
    assert re.match(file_filter.fileType, "document.txt")
    assert re.match(file_filter.fileType, "report.pdf")
    assert not re.match(file_filter.fileType, "image.png")

def test_set_file_type_with_invalid_extension(file_filter):
    # Set an invalid file type and check if it works as expected (no matches)
    file_filter.setFileType("[invalid]")  # This is a strange pattern, but it won't raise an error
    assert not re.match(file_filter.fileType, "example.txt")
    assert not re.match(file_filter.fileType, "example.pdf")
    
    # Test with an empty file extension, should not match anything
    file_filter.setFileType("")
    assert not re.match(file_filter.fileType, "example.txt")


def test_set_file_type_with_special_characters(file_filter):
    # Test with special characters in file extensions
    file_filter.setFileType("t.x.t")
    assert re.match(file_filter.fileType, "example.t.x.t")
    assert not re.match(file_filter.fileType, "example.txt")

def test_set_file_type_with_uppercase_extensions(file_filter):
    # Test with uppercase file extensions
    file_filter.setFileType("TXT")
    assert re.match(file_filter.fileType, "file.TXT")
    assert not re.match(file_filter.fileType, "file.txt")

