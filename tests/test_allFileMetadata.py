import os
import time
import pytest
import threading
import tempfile
from unittest.mock import patch
from twinTrim.dataStructures.allFileMetadata import AllFileMetadata
from twinTrim.dataStructures.allFileMetadata import add_or_update_file, store, store_lock
from twinTrim.utils import get_file_hash

# Fixtures
@pytest.fixture
def temp_file(tmp_path):
    """Fixture to create a temporary file for testing."""
    temp_file_path = tmp_path / "test_file.txt"
    with open(temp_file_path, "w") as f:
        f.write("Sample content")
    return str(temp_file_path)

@pytest.fixture(autouse=True)
def reset_store():
    """Fixture to reset the store before each test."""
    store.clear()

# Mocking the get_file_hash function
def mock_get_file_hash(file_path):
    return f"hash_{file_path}"

@pytest.fixture(autouse=True)
def mock_file_hash_function(monkeypatch):
    """Mock get_file_hash to provide predictable outputs for tests."""
    monkeypatch.setattr("twinTrim.dataStructures.allFileMetadata.get_file_hash", mock_get_file_hash)

# Test cases
def test_add_new_file_metadata(temp_file):
    store.clear()
    add_or_update_file(temp_file)
    file_hash = mock_get_file_hash(temp_file)

    assert file_hash in store, "File hash should be in the store after adding"
    assert store[file_hash].filepath == temp_file, "Stored file path should match the added file"


def test_add_or_update_file_concurrently():
    file_paths = ["file_1", "file_2", "file_3"]

    def worker(file_path):
        add_or_update_file(file_path)

    threads = [threading.Thread(target=worker, args=(file_path,)) for file_path in file_paths]

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    assert len(store) == 3
    assert all(f"hash_{file_path}" in store for file_path in file_paths)
    for file_path in file_paths:
        assert store[f"hash_{file_path}"].filepath == file_path

def test_add_or_update_file_with_duplicates_concurrently():
    file_paths = ["file_1", "file_1", "file_1"]

    def worker(file_path):
        add_or_update_file(file_path)

    threads = [threading.Thread(target=worker, args=(file_path,)) for file_path in file_paths]

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    assert len(store) == 1
    assert "hash_file_1" in store
    assert store["hash_file_1"].filepath == "file_1"

def test_add_or_update_file_mixed_concurrently():
    file_paths = ["file_1", "file_1", "file_2", "file_3", "file_3"]

    def worker(file_path):
        add_or_update_file(file_path)

    threads = [threading.Thread(target=worker, args=(file_path,)) for file_path in file_paths]

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

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

@pytest.fixture
def setup_files():
    temp_file1 = tempfile.NamedTemporaryFile(delete=False)
    temp_file2 = tempfile.NamedTemporaryFile(delete=False)

    temp_file1.write(b'Initial content for file 1.')
    temp_file1.close()

    temp_file2.write(b'Initial content for file 2.')
    temp_file2.close()

    yield temp_file1.name, temp_file2.name

    if os.path.exists(temp_file1.name):
        os.remove(temp_file1.name)
    if os.path.exists(temp_file2.name):
        os.remove(temp_file2.name)

def test_compare_and_replace_removes_correct_file(setup_files):
    file1, file2 = setup_files

    with patch('os.path.getmtime') as mock_getmtime, \
         patch('twinTrim.dataStructures.allFileMetadata.handle_and_remove') as mock_remove:  
        
        mock_getmtime.side_effect = lambda path: 1000 if path == file1 else 2000

        metadata1 = AllFileMetadata(file1)
        metadata2 = AllFileMetadata(file2)

        metadata1.compare_and_replace(metadata2)

        mock_remove.assert_called_once_with(file1)

def test_compare_and_replace_no_file_removed_when_file_missing(setup_files):
    file1, _ = setup_files
    metadata1 = AllFileMetadata(file1)
    nonexistent_file = 'nonexistent_file.txt'
    metadata2 = AllFileMetadata(nonexistent_file)

    with patch('twinTrim.utils.handle_and_remove') as mock_remove:
        metadata1.compare_and_replace(metadata2)
        mock_remove.assert_not_called()

def test_compare_and_replace_no_file_removed_when_both_files_missing(setup_files):
    file1, _ = setup_files
    metadata1 = AllFileMetadata(file1)
    nonexistent_file1 = 'nonexistent_file1.txt'
    nonexistent_file2 = 'nonexistent_file2.txt'
    metadata2 = AllFileMetadata(nonexistent_file1)
    metadata3 = AllFileMetadata(nonexistent_file2)

    with patch('twinTrim.utils.handle_and_remove') as mock_remove:
        metadata1.compare_and_replace(metadata2)
        mock_remove.assert_not_called()

    with patch('twinTrim.utils.handle_and_remove') as mock_remove:
        metadata1.compare_and_replace(metadata3)
        mock_remove.assert_not_called()
