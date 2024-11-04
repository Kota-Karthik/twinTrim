import os
import pytest
from twinTrim.dataStructures.allFileMetadata import AllFileMetadata
from pathlib import Path

@pytest.fixture
def temp_file(tmp_path):
    """Creates a temporary file for testing and returns its Path object."""
    file = tmp_path / "test_file.txt"
    file.write_text("Sample content")
    return file  # Return Path object instead of str

def test_get_modification_time_existing_file(temp_file):
    """
    Test that the modification time is correctly retrieved for an existing file.
    """
    # Arrange
    metadata = AllFileMetadata(temp_file)

    # Act
    modification_time = metadata.get_modification_time()

    # Assert
    assert modification_time > 0, (
        "Expected a positive modification time for an existing file, but got None or 0"
    )

def test_get_modification_time_non_existing_file():
    """
    Test that the modification time retrieval returns -1 or appropriate error for non-existing file.
    """
    # Arrange
    non_existing_filepath = Path("non/existing/path/file.txt")
    metadata = AllFileMetadata(non_existing_filepath)

    # Act
    modification_time = metadata.get_modification_time()

    # Assert
    assert modification_time == -1, (
        "Expected -1 for modification time of non-existing file, but got a different value"
    )
