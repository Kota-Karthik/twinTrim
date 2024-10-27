import os
import pytest
import tempfile
from twinTrim.dataStructures.allFileMetadata import AllFileMetadata
from unittest.mock import patch

@pytest.fixture
def setup_files():
    # Create two temporary files for testing
    temp_file1 = tempfile.NamedTemporaryFile(delete=False)
    temp_file2 = tempfile.NamedTemporaryFile(delete=False)

    # Write some initial content to the files
    temp_file1.write(b'Initial content for file 1.')
    temp_file1.close()

    temp_file2.write(b'Initial content for file 2.')
    temp_file2.close()

    # Return the paths of the temporary files
    yield temp_file1.name, temp_file2.name

    # Cleanup - only remove if the file still exists
    if os.path.exists(temp_file1.name):
        os.remove(temp_file1.name)
    if os.path.exists(temp_file2.name):
        os.remove(temp_file2.name)

def test_compare_and_replace_removes_correct_file(setup_files):
    file1, file2 = setup_files

    # Use patch to mock modification times and handle_and_remove function
    with patch('os.path.getmtime') as mock_getmtime, \
         patch('twinTrim.dataStructures.allFileMetadata.handle_and_remove') as mock_remove:  
        
        # Set mock modification times: file1 older than file2
        mock_getmtime.side_effect = lambda path: 1000 if path == file1 else 2000

        metadata1 = AllFileMetadata(file1)
        metadata2 = AllFileMetadata(file2)

        # Execute compare_and_replace
        metadata1.compare_and_replace(metadata2)

        # Verify that file1 was "removed" since it is older
        mock_remove.assert_called_once_with(file1)

def test_compare_and_replace_no_file_removed_when_file_missing(setup_files):
    file1, _ = setup_files

    # Create a metadata object for file1
    metadata1 = AllFileMetadata(file1)

    # Create a metadata object for a non-existing file
    nonexistent_file = 'nonexistent_file.txt'
    metadata2 = AllFileMetadata(nonexistent_file)

    with patch('twinTrim.utils.handle_and_remove') as mock_remove:
        metadata1.compare_and_replace(metadata2)

        # Check that no file is removed
        mock_remove.assert_not_called()

def test_compare_and_replace_no_file_removed_when_both_files_missing(setup_files):
    file1, _ = setup_files

    # Create a metadata object for file1
    metadata1 = AllFileMetadata(file1)

    # Create metadata objects for two non-existing files
    nonexistent_file1 = 'nonexistent_file1.txt'
    nonexistent_file2 = 'nonexistent_file2.txt'
    metadata2 = AllFileMetadata(nonexistent_file1)
    metadata3 = AllFileMetadata(nonexistent_file2)

    with patch('twinTrim.utils.handle_and_remove') as mock_remove:
        metadata1.compare_and_replace(metadata2)
        # No file should be removed since the second file doesn't exist
        mock_remove.assert_not_called()

    with patch('twinTrim.utils.handle_and_remove') as mock_remove:
        metadata1.compare_and_replace(metadata3)
        # No file should be removed since the second file doesn't exist
        mock_remove.assert_not_called()