import pytest
import os
from twinTrim.dataStructures.allFileMetadata import AllFileMetadata

# Create a temporary file for testing
@pytest.fixture
def temp_file(tmp_path):
    test_file = tmp_path / "test_file.txt"
    test_file.write_text("Hello, World!")
    return str(test_file)

def test_get_modification_time_existing_file(temp_file):
    # Arrange
    metadata = AllFileMetadata()
    # Act
    modification_time = metadata.get_modification_time(temp_file)
    # Assert
    assert modification_time != -1  # Ensure it returns a valid timestamp

def test_get_modification_time_non_existing_file():
    # Arrange
    metadata = AllFileMetadata()
    non_existing_file = "non_existing_file.txt"
    # Act
    modification_time = metadata.get_modification_time(non_existing_file)
    # Assert
    assert modification_time == -1  # Ensure it returns -1 for non-existing file
