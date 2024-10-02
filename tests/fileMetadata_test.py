import threading
import pytest
from twinTrim.dataStructures.fileMetadata import (
    add_or_update_normal_file,
    normalStore,
    normalStore_lock,
)

# Mocking the get_file_hash function to return a predictable hash
def mock_get_file_hash(file_path):
    return f"hash_{file_path}"

# Automatically replace the get_file_hash function with the mock in all tests
@pytest.fixture(autouse=True)
def mock_get_file_hash_func(monkeypatch):
    # Replace get_file_hash in the module where it's used
    monkeypatch.setattr(
        "twinTrim.dataStructures.fileMetadata.get_file_hash", mock_get_file_hash
    )

# Automatically reset the normalStore before each test
@pytest.fixture(autouse=True)
def reset_normal_store():
    normalStore.clear()

def test_add_or_update_normal_file_concurrently():
    """
    Test that normalStore is consistent when add_or_update_normal_file is called
    concurrently with different file paths by multiple threads.
    """
    # List of file paths to be added concurrently
    file_paths = [f"file_{i}" for i in range(10)]

    # Function to be called by each thread to add a file path
    def worker(file_path):
        add_or_update_normal_file(file_path)

    # Create threads for concurrent execution
    threads = [threading.Thread(target=worker, args=(fp,)) for fp in file_paths]

    # Start all the threads
    for thread in threads:
        thread.start()

    # Wait for all the threads to finish
    for thread in threads:
        thread.join()

    # Assert that normalStore has exactly 10 unique file hashes
    assert len(normalStore) == 10

    # Assert that each file hash corresponds to the correct file path
    for file_path in file_paths:
        file_hash = mock_get_file_hash(file_path)
        assert file_hash in normalStore
        assert normalStore[file_hash].filepaths == [file_path]

def test_add_or_update_normal_file_with_duplicates_concurrently():
    """
    Test that adding duplicate file paths to normalStore does not create duplicate entries.
    """
    file_path = "duplicate_file.txt"
    num_threads = 5

    # Function to be called by each thread to add the same file path
    def worker():
        add_or_update_normal_file(file_path)

    # Create threads to add the same file path concurrently
    threads = [threading.Thread(target=worker) for _ in range(num_threads)]

    # Start all the threads
    for thread in threads:
        thread.start()

    # Wait for all the threads to finish
    for thread in threads:
        thread.join()

    # Assert that normalStore has exactly 1 unique file hash
    file_hash = mock_get_file_hash(file_path)
    assert len(normalStore) == 1
    assert file_hash in normalStore

    # Assert that the file path is added only once
    assert normalStore[file_hash].filepaths == [file_path]
