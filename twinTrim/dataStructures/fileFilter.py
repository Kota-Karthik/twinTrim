import os
import re

class FileFilter:
    def __init__(self):
        self.minFileSize = "10kb"
        self.maxFileSize = "1gb"
        self.fileType = r"^.+\.*$" 
        self.fileExclude = []

    def setMinFileSize(self, size):
        self.minFileSize = size

    def setMaxFileSize(self, size):
        self.maxFileSize = size

    def setFileType(self, file_type):
        self.fileType = rf"^.+\.{file_type}$"  

    def addFileExclude(self, file_name):
        self.fileExclude.append(file_name)

    def filter_files(self, file_path):
        """Check if a file meets the filter criteria."""
        if os.path.getsize(file_path) < self.minFileSize or os.path.getsize(file_path) > self.maxFileSize:
            return False
        if not re.match(self.fileType, os.path.basename(file_path)):  
            return False
        if os.path.basename(file_path).strip() in self.fileExclude:
            return False
        return True

import pytest

# PyTest setup
@pytest.fixture
def file_filter():
    return FileFilter()

# Test functions
@pytest.mark.unit
def test_add_file_exclude(file_filter):
    file_filter.addFileExclude("test.txt")
    assert "test.txt" in file_filter.fileExclude
    assert len(file_filter.fileExclude) == 1

    file_filter.addFileExclude("example.pdf")
    assert "example.pdf" in file_filter.fileExclude
    assert len(file_filter.fileExclude) == 2

    file_filter.addFileExclude("file with spaces.doc")
    assert "file with spaces.doc" in file_filter.fileExclude
    assert len(file_filter.fileExclude) == 3

    file_filter.addFileExclude("")
    assert "" in file_filter.fileExclude
    assert len(file_filter.fileExclude) == 4

@pytest.mark.unit
def test_add_file_exclude_multiple_calls(file_filter):
    file_filter.addFileExclude("file1.txt")
    file_filter.addFileExclude("file2.txt")
    file_filter.addFileExclude("file3.txt")
    
    assert all(file in file_filter.fileExclude for file in ["file1.txt", "file2.txt", "file3.txt"])
    assert len(file_filter.fileExclude) == 3

@pytest.mark.unit
def test_add_file_exclude_duplicates(file_filter):
    file_filter.addFileExclude("duplicate.txt")
    file_filter.addFileExclude("duplicate.txt")
    
    assert "duplicate.txt" in file_filter.fileExclude
    assert len(file_filter.fileExclude) == 2
    assert file_filter.fileExclude.count("duplicate.txt") == 2

if __name__ == "__main__":
    pytest.main([__file__])