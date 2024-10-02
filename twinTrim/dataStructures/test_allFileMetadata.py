import pytest
import os
from twinTrim.dataStructures.allFileMetadata import AllFileMetadata
import pytest


@pytest.fixture
def temp_file(tmp_path):
    # Create a temporary file for testing
    file = tmp_path / "test_file.txt"
    file.write_text("Sample content")
    return str(file)

def test_get_modification_time_existing_file(temp_file):
    # Arrange
    metadata = AllFileMetadata(temp_file)
    # Act
    modification_time = metadata.get_modification_time()
    # Assert
    assert modification_time is not None  # Replace with appropriate assertion
    
def test_get_modification_time_non_existing_file():
    # Arrange
    non_existing_filepath = "path/to/non/existing/file.txt"
    metadata = AllFileMetadata(non_existing_filepath)
    # Act
    modification_time = metadata.get_modification_time()
    # Assert
    assert modification_time == -1  # Update the assertion
