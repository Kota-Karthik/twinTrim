import pytest
import threading
from twinTrim.dataStructures.allFileMetadata import AllFileMetadata
from twinTrim.dataStructures.allFileMetadata import add_or_update_file, store, store_lock

# Mocking the get_file_hash function for different file paths
def mock_get_file_hash(file_path):
  return f"hash_{file_path}"

# Reset the store before each test
@pytest.fixture(autouse=True)
def reset_store():
  store.clear()

# Mocking the get_file_hash function for testing so that it doesn't use the actual function
@pytest.fixture(autouse=True)
def mock_file_hash_function(monkeypatch):
  monkeypatch.setattr("twinTrim.dataStructures.allFileMetadata.get_file_hash", mock_get_file_hash)

def test_add_or_update_file_concurrently():
  "Test that the store remains consistent when multiple threads call add_or_update_file with different file paths concurrently"
  
  file_paths = ["file_1", "file_2", "file_3"]
  
  # Function to add or update file in the store
  def worker(file_path):
    add_or_update_file(file_path)
    
  # Create threads for concurrent execution
  threads = [threading.Thread(target=worker, args=(file_path,)) for file_path in file_paths]
  
  # Start all threads
  for thread in threads:
    thread.start()
    
  # Wait for all threads to finish
  for thread in threads:
    thread.join()
    
  # Checking that the store contains all the unique file hashes
  assert len(store) == 3
  assert "hash_file_1" in store
  assert "hash_file_2" in store
  assert "hash_file_3" in store
  assert store["hash_file_1"].filepath == "file_1"
  assert store["hash_file_2"].filepath == "file_2"
  assert store["hash_file_3"].filepath == "file_3"
  
def test_add_or_update_file_with_duplicates_concurrently():
  "Test that the store remains consistent when multiple threads call add_or_update_file with the same file paths concurrently"
  
  file_paths = ["file_1", "file_1", "file_1"]
  
  # Function to add or update file in the store
  def worker(file_path):
    add_or_update_file(file_path)
    
  # Create threads for concurrent execution
  threads = [threading.Thread(target=worker, args=(file_path,)) for file_path in file_paths]
  
  # Start all threads
  for thread in threads:
    thread.start()
    
  # Wait for all threads to finish
  for thread in threads:
    thread.join()
    
  # Checking that the store contains only one unique file hash
  assert len(store) == 1
  assert "hash_file_1" in store
  assert store["hash_file_1"].filepath == "file_1"
  
def test_add_or_update_file_mixed_concurrently():
  "Test that the store remains consistent when multiple threads call add_or_update_file with both unique and duplicate file paths concurrently"
  
  file_paths = ["file_1", "file_1", "file_2", "file_3", "file_3"]
  
  # Function to add or update file in the store
  def worker(file_path):
    add_or_update_file(file_path)
    
  # Create threads for concurrent execution
  threads = [threading.Thread(target=worker, args=(file_path,)) for file_path in file_paths]
  
  # Start all threads
  for thread in threads:
    thread.start()
    
  # Wait for all threads to finish
  for thread in threads:
    thread.join()
    
  # Checking that the store contains all the unique file hashes
  # file_1 and file_3 are duplicates so only one of them should be present in the store
  assert len(store) == 3
  assert "hash_file_1" in store
  assert "hash_file_2" in store
  assert "hash_file_3" in store
  assert store["hash_file_1"].filepath == "file_1"
  assert store["hash_file_2"].filepath == "file_2"
  assert store["hash_file_3"].filepath == "file_3"

def test_add_or_update_file_when_file_doesnt_exist(mocker):
    mockfile = "mockfile.txt"
    mocker.patch("twinTrim.dataStructures.allFileMetadata.os.path.exists", return_value=False)
    mocker.patch("twinTrim.dataStructures.allFileMetadata.get_file_hash", side_effect=FileNotFoundError)
    
    with pytest.raises(FileNotFoundError):
        add_or_update_file(mockfile)
