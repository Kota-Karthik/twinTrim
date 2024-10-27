import pytest
import os
import time
from twinTrim.dataStructures.allFileMetadata import AllFileMetadata, add_or_update_file, store
from twinTrim.utils import get_file_hash

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

# New tests for add_or_update_file function

def test_add_new_file_metadata(temp_file):
    # Clear the store before test
    store.clear()
    # Act
    add_or_update_file(temp_file)
    file_hash = get_file_hash(temp_file)
    
    # Assert
    assert file_hash in store, "File hash should be present in the store after adding"
    assert store[file_hash].filepath == temp_file, "Stored filepath should match the added file path"

def test_update_existing_file_metadata(temp_file):
    # Arrange: Add the initial file
    store.clear()
    add_or_update_file(temp_file)
    file_hash = get_file_hash(temp_file)
    
    # Verify that the initial file is added to the store
    assert file_hash in store
    original_file_path = store[file_hash].filepath

    # Create a new file with the same content but a different modification time
    new_file = os.path.join(os.path.dirname(temp_file), "new_test_file.txt")
    with open(new_file, "w") as f:
        f.write("Sample content")
    time.sleep(2)  # Ensure the new file has a different modification time

    # Act: Add the new file with the same hash
    add_or_update_file(new_file)
    
    # Assert: Check if the store has been updated to the latest file path
    assert file_hash in store, "File hash should be present in the store after updating"
    assert store[file_hash].filepath == new_file, (
        f"Expected latest file path '{new_file}', but got '{store[file_hash].filepath}'"
    )
    assert store[file_hash].filepath != original_file_path, (
        "Store should replace the old file path with the latest one"
    )
