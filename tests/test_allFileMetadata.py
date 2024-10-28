import os
import time
import pytest
from twinTrim.dataStructures.allFileMetadata import add_or_update_file, store
from twinTrim.utils import get_file_hash

@pytest.fixture
def temp_file(tmp_path):
    """Fixture to create a temporary file for testing."""
    temp_file_path = tmp_path / "test_file.txt"
    with open(temp_file_path, "w") as f:
        f.write("Sample content")
    return str(temp_file_path)

def test_add_new_file_metadata(temp_file):
    # Arrange: Clear the store and add a new file
    store.clear()
    add_or_update_file(temp_file)
    file_hash = get_file_hash(temp_file)

    # Assert: Check if the file was added to the store
    assert file_hash in store, "File hash should be in the store after adding"
    assert store[file_hash].filepath == temp_file, "Stored file path should match the added file"

def test_update_existing_file_metadata(temp_file, tmp_path):
    # Arrange: Clear the store, add the initial file
    store.clear()
    add_or_update_file(temp_file)
    file_hash = get_file_hash(temp_file)

    # Verify the initial file is added
    assert file_hash in store
    original_file_path = store[file_hash].filepath

    # Create a new file with the same content but a different modification time
    new_file = tmp_path / "new_test_file.txt"
    with open(new_file, "w") as f:
        f.write("Sample content")
    
    # Wait to ensure modification time is different
    time.sleep(1)
    os.utime(new_file, (new_file.stat().st_atime, time.time()))

    # Act: Update the store with the new file having the same hash
    add_or_update_file(str(new_file))

    # Assert: Verify the store is updated with the latest file path
    assert file_hash in store, "File hash should still be in the store after updating"
    assert store[file_hash].filepath == str(new_file), (
        f"Expected latest file path '{new_file}', but got '{store[file_hash].filepath}'"
    )
