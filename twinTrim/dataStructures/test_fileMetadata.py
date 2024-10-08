# test_fileMetadata.py
import pytest
from twinTrim.dataStructures.fileMetadata import FileMetadata

def test_insert_new_file():
    # Test inserting a new file into the metadata
    metadata = FileMetadata([])
    file_path = "/path/to/file1.txt"
    
    metadata.insert_file(file_path)
    
    assert len(metadata.filepaths) == 1
    assert metadata.filepaths[0] == file_path

def test_insert_duplicate_file():
    # Test trying to insert a file that is already present
    file_path = "/path/to/file2.txt"
    metadata = FileMetadata([file_path])
    
    metadata.insert_file(file_path)
    
    # The file should not be added again
    assert len(metadata.filepaths) == 1
    assert metadata.filepaths[0] == file_path

def test_insert_multiple_files():
    # Test inserting multiple different files
    file_path1 = "/path/to/file3.txt"
    file_path2 = "/path/to/file4.txt"
    
    metadata = FileMetadata([file_path1])
    
    metadata.insert_file(file_path2)
    
    assert len(metadata.filepaths) == 2
    assert file_path1 in metadata.filepaths
    assert file_path2 in metadata.filepaths
