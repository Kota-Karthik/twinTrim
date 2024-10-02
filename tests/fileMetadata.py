import threading
import pytest
from twinTrim.dataStructures.fileMetadata import add_or_update_normal_file, normalStore, normalStore_lock

# Mocking the get_file_hash function so that we don't have to worry about the actual file
def mock_get_file_hash(file_path):
    return f"hash_{file_path}"
  
# This will automatically replaces the get_file_hash function with the mock_get_file_hash function
@pytest.fixture(autouse=True)
def mock_get_file_hash_func(monkeypatch):
    monkeypatch.setattr("twinTrim.dataStructures.fileMetadata.get_file_hash", mock_get_file_hash)
    
# Automatically reset the normalStore before each test
@pytest.fixture(autouse=True)
def reset_normal_store():
    normalStore.clear()
    
def test_add_or_update_normal_file_concurrently():
  "Test that normalStore is consistant when add_or_update_normal_file is called concurrently with different file paths by multiple threads"
  
  # List of file paths to be added concurrently
  file_paths = [f"file_{i}" for i in range(10)]
  
  # this function will be called by each thread to add a file path
  def worker(file_path):
    add_or_update_normal_file(file_path)
    
  # Threads for concurrent execution
  threads = [threading.Thread(target=worker, args=(file_path,)) for file_path in file_paths]
  
  # starting all the threads for concurrent execution
  for thread in threads:
    thread.start()
    
  # waiting for all the threads to finish
  for thread in threads:
    thread.join()
    
  # Checking that normalStore has exactly 10 unique file hashes (since all file paths are unique)
  assert len(normalStore) == 10
  
  # Checking that each file hash has exactly 1 file path
  for file_path in file_paths:
    file_hash = mock_get_file_hash(file_path)
    assert file_hash in normalStore
    assert normalStore[file_hash].filepaths == [file_path]
    
def test_add_or_update_normal_file_with_duplicates_concurrently():
  "Test that adding duplicate file paths to normalStore does not create duplicate entries"
  
  file_paths = "duplicate_file.txt"
  num_threads = 5
  
  # this function will be called by each thread to add a file path
  def worker():
    add_or_update_normal_file(file_paths)
    
  # Create a list of threads to add the same file path concurrently
  threads = [threading.Thread(target=worker) for _ in range(num_threads)]
  
  # starting all the threads for concurrent execution
  for thread in threads:
    thread.start()
    
  # waiting for all the threads to finish
  for thread in threads:
    thread.join()
    
  # Checking that normalStore has exactly 1 unique file hash (since all file paths are the same)
  file_hash = mock_get_file_hash(file_paths)
  assert len(normalStore) == 1
  assert file_hash in normalStore
  
  # Checking that the file path is added only once despite being added by multiple threads
  assert normalStore[file_hash].filepaths == [file_paths]