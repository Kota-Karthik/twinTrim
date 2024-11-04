import pytest
import os
from twinTrim.dataStructures.allFileMetadata import AllFileMetadata
import pytest

from twinTrim.dataStructures.allFileMetadata import AllFileMetadata

@pytest.fixture
def temp_file(tmp_path):
    # Create a temporary file for testing
    """Creates a temporary file with content and returns its path."""
    file = tmp_path / "test_file.txt"
    file.write_text("Sample content")
    return str(file)

def test_get_modification_time_existing_file(temp_file):
    """
    Test that the modification time is correctly retrieved for an existing file.
    """
    # Arrange
    metadata = AllFileMetadata(temp_file)

    # Act
    modification_time = metadata.get_modification_time()

    # Assert
    assert modification_time is not None  # Replace with appropriate assertion

def test_get_modification_time_non_existing_file():
    assert isinstance(modification_time, float), "Expected modification time as a float"
    assert modification_time > 0, "Expected a valid modification time, but got 0 or a negative value"

def test_get_modification_time_non_existing_file(tmp_path):
    """
    Test that the modification time retrieval returns -1 for a non-existing file.
    """
    # Arrange
    non_existing_filepath = "path/to/non/existing/file.txt"
    metadata = AllFileMetadata(non_existing_filepath)
    non_existing_filepath = tmp_path / "non_existent_file.txt"
    metadata = AllFileMetadata(str(non_existing_filepath))

    # Act
    modification_time = metadata.get_modification_time()

    # Assert
    assert modification_time == -1  # Update the assertion
    assert modification_time == -1, "Expected -1 for non-existing file modification time"
Footer
