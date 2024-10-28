# test_fileMetadata.py
from unittest.mock import mock_open, patch
import pytest
from twinTrim.dataStructures.fileMetadata import normalStore, add_or_update_normal_file, FileMetadata

def test_insert_new_file():
    # Test inserting a new file into the metadata
    metadata = FileMetadata([])
    file_path = "C:\\Users\\2004s\\Desktop\\dummy\\dummy_1.txt"
    
    metadata.insert_file(file_path)
    
    assert len(metadata.filepaths) == 1
    assert metadata.filepaths[0] == file_path

def test_insert_duplicate_file():
    # Test trying to insert a file that is already present
    file_path = "C:\\Users\\2004s\\Desktop\\dummy\\dummy_2.txt"
    metadata = FileMetadata([file_path])
    
    metadata.insert_file(file_path)
    
    # The file should not be added again
    assert len(metadata.filepaths) == 1
    assert metadata.filepaths[0] == file_path

def test_insert_multiple_files():
    # Test inserting multiple different files
    file_path1 = "C:\\Users\\2004s\\Desktop\\dummy\\dummy_3.txt"
    file_path2 = "C:\\Users\\2004s\\Desktop\\dummy\\dummy_4.txt"
    
    metadata = FileMetadata([file_path1])
    
    metadata.insert_file(file_path2)
    
    assert len(metadata.filepaths) == 2
    assert file_path1 in metadata.filepaths
    assert file_path2 in metadata.filepaths

def test_add_or_update_new_file():
    file_path = "C:\\Users\\2004s\\Desktop\\dummy\\dummy_5.txt"  # Define the mock file path
    expected_file_hash = "b1295d8ebb927df19ad74eec6aea72e3"  # Use the actual hash computed from the file

    # Mock the get_file_hash function to return the expected hash
    with patch("twinTrim.utils.get_file_hash", return_value=expected_file_hash), \
         patch("builtins.open", mock_open(read_data=b"some binary content")):

        # Clear normalStore before the test to avoid conflicts
        normalStore.clear()

        # Call the function to add a new file
        add_or_update_normal_file(file_path)

        # Check that the expected file hash is in normalStore
        assert expected_file_hash in normalStore.keys(), f"Expected hash '{expected_file_hash}' not found in normalStore"

        # Check that the file path was added correctly
        assert normalStore[expected_file_hash].filepaths == [file_path], "File path not added correctly"

def test_add_or_update_existing_file():
    file_path1 = "C:\\Users\\2004s\\Desktop\\dummy\\dummy_5.txt"
    file_path2 = "C:\\Users\\2004s\\Desktop\\dummy\\dummy_5_v2.txt"
    expected_file_hash = "b1295d8ebb927df19ad74eec6aea72e3"  # Use the actual hash computed from the file

    # First add a file
    with patch("twinTrim.utils.get_file_hash", return_value=expected_file_hash), \
         patch("builtins.open", mock_open(read_data=b"some binary content")):
        normalStore.clear()
        add_or_update_normal_file(file_path1)

    # Then update it
    with patch("twinTrim.utils.get_file_hash", return_value=expected_file_hash), \
         patch("builtins.open", mock_open(read_data=b"some binary content")):
        add_or_update_normal_file(file_path2)

    # Check that the file paths were updated correctly
    assert expected_file_hash in normalStore.keys(), f"Expected hash '{expected_file_hash}' not found in normalStore"
    assert normalStore[expected_file_hash].filepaths == [file_path1, file_path2], "File paths not updated correctly"