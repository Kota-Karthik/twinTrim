import os
import pytest
import tempfile
import time
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

    # Cleanup
    os.remove(temp_file1.name)
    os.remove(temp_file2.name)

def test_compare_and_replace_removes_correct_file(setup_files):
    file1, file2 = setup_files

    # Modify the modification time of the second file to be newer
    time.sleep(1)  # Ensure file2 is modified after file1
    os.utime(file2, None)

    metadata1 = AllFileMetadata(file1)
    metadata2 = AllFileMetadata(file2)

    with patch('twinTrim.dataStructures.allFileMetadata.handle_and_remove') as mock_remove:
        metadata1.compare_and_replace(metadata2)

        # Check that file1 is removed
        mock_remove.assert_called_once_with(file1)

def test_compare_and_replace_no_file_removed_when_file_missing(setup_files):
    file1, file2 = setup_files

    # Create a metadata object for file1
    metadata1 = AllFileMetadata(file1)

    # Create a metadata object for a non-existing file
    nonexistent_file = 'nonexistent_file.txt'
    metadata2 = AllFileMetadata(nonexistent_file)

    with patch('twinTrim.dataStructures.allFileMetadata.handle_and_remove') as mock_remove:
        metadata1.compare_and_replace(metadata2)

        # Check that no file is removed
        mock_remove.assert_not_called()

def test_compare_and_replace_no_file_removed_when_both_files_missing(setup_files):
    file1, _ = setup_files

    # Create a metadata object for file1
    metadata1 = AllFileMetadata(file1)

    # Create a metadata object for two non-existing files
    nonexistent_file1 = 'nonexistent_file1.txt'
    nonexistent_file2 = 'nonexistent_file2.txt'
    metadata2 = AllFileMetadata(nonexistent_file1)
    metadata3 = AllFileMetadata(nonexistent_file2)

    with patch('twinTrim.dataStructures.allFileMetadata.handle_and_remove') as mock_remove:
        metadata1.compare_and_replace(metadata2)
        # No file should be removed since the second file doesn't exist
        mock_remove.assert_not_called()

    with patch('twinTrim.dataStructures.allFileMetadata.handle_and_remove') as mock_remove:
        metadata1.compare_and_replace(metadata3)
        # No file should be removed since the second file doesn't exist
        mock_remove.assert_not_called()