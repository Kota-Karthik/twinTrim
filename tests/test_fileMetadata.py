import pytest
from unittest.mock import patch, mock_open
from twinTrim.dataStructures.fileMetadata import (
    add_or_update_normal_file,
    normalStore,
    FileMetadata,
    normalStore_lock,
)
import threading
import os
import tempfile

# Mock the get_file_hash function to return a predictable hash
def mock_get_file_hash(file_path):
    return f"hash_{file_path}"

# Automatically replace the get_file_hash function with the mock in all tests
@pytest.fixture(autouse=True)
def mock_get_file_hash_func(monkeypatch):
    monkeypatch.setattr(
        "twinTrim.dataStructures.fileMetadata.get_file_hash", mock_get_file_hash
    )

# Automatically reset the normalStore before each test
@pytest.fixture(autouse=True)
def reset_normal_store():
    normalStore.clear()

# Test inserting a new file
def test_insert_new_file():
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        file_path = temp_file.name
        metadata = FileMetadata([])
        metadata.insert_file(file_path)

        assert len(metadata.filepaths) == 1
        assert metadata.filepaths[0] == file_path

# Test inserting a duplicate file
def test_insert_duplicate_file():
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        file_path = temp_file.name
        metadata = FileMetadata([file_path])
        metadata.insert_file(file_path)

        assert len(metadata.filepaths) == 1
        assert metadata.filepaths[0] == file_path

# Test inserting multiple files
def test_insert_multiple_files():
    with tempfile.NamedTemporaryFile(delete=False) as temp_file1, tempfile.NamedTemporaryFile(delete=False) as temp_file2:
        file_path1 = temp_file1.name
        file_path2 = temp_file2.name

        metadata = FileMetadata([file_path1])
        metadata.insert_file(file_path2)

        assert len(metadata.filepaths) == 2
        assert file_path1 in metadata.filepaths
        assert file_path2 in metadata.filepaths

# Test adding or updating a new file
def test_add_or_update_new_file():
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        file_path = temp_file.name
        expected_file_hash = "hash_" + file_path

        with patch("builtins.open", mock_open(read_data=b"some binary content")):
            normalStore.clear()
            add_or_update_normal_file(file_path)

            assert expected_file_hash in normalStore
            assert normalStore[expected_file_hash].filepaths == [file_path]

# Test adding a new file to an empty store
def test_add_new_file_to_empty_store():
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        file_path = temp_file.name
        expected_file_hash = "hash_" + file_path

        with patch("builtins.open", mock_open(read_data=b"some binary content")):
            normalStore.clear()
            add_or_update_normal_file(file_path)

            assert len(normalStore) == 1
            assert expected_file_hash in normalStore
            assert normalStore[expected_file_hash].filepaths == [file_path]


# Test no duplicate insertion in metadata
def test_no_duplicate_insertion_in_metadata():
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        file_path = temp_file.name
        expected_file_hash = "hash_" + file_path

        with patch("builtins.open", mock_open(read_data=b"some binary content")):
            normalStore.clear()
            add_or_update_normal_file(file_path)
            add_or_update_normal_file(file_path)

            assert len(normalStore) == 1
            assert expected_file_hash in normalStore
            assert normalStore[expected_file_hash].filepaths == [file_path]

# Test adding multiple files with different hashes
def test_multiple_files_different_hashes():
    with tempfile.NamedTemporaryFile(delete=False) as temp_file1, tempfile.NamedTemporaryFile(delete=False) as temp_file2, tempfile.NamedTemporaryFile(delete=False) as temp_file3:
        file_path1 = temp_file1.name
        file_path2 = temp_file2.name
        file_path3 = temp_file3.name

        with patch("builtins.open", mock_open(read_data=b"some binary content")):
            normalStore.clear()
            add_or_update_normal_file(file_path1)
            add_or_update_normal_file(file_path2)
            add_or_update_normal_file(file_path3)

            assert len(normalStore) == 3
            assert "hash_" + file_path1 in normalStore and normalStore["hash_" + file_path1].filepaths == [file_path1]
            assert "hash_" + file_path2 in normalStore and normalStore["hash_" + file_path2].filepaths == [file_path2]
            assert "hash_" + file_path3 in normalStore and normalStore["hash_" + file_path3].filepaths == [file_path3]

# Test concurrent add or update
def test_add_or_update_normal_file_concurrently():
    file_paths = [f"file_{i}.txt" for i in range(10)]

    def worker(file_path):
        add_or_update_normal_file(file_path)

    threads = [threading.Thread(target=worker, args=(fp,)) for fp in file_paths]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    assert len(normalStore) == 10
    for file_path in file_paths:
        file_hash = "hash_" + file_path
        assert file_hash in normalStore
        assert normalStore[file_hash].filepaths == [file_path]

# Test adding duplicates concurrently
def test_add_or_update_normal_file_with_duplicates_concurrently():
    file_path = "duplicate_file.txt"
    num_threads = 5

    def worker():
        add_or_update_normal_file(file_path)

    threads = [threading.Thread(target=worker) for _ in range(num_threads)]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    file_hash = "hash_" + file_path
    assert len(normalStore) == 1
    assert file_hash in normalStore
    assert normalStore[file_hash].filepaths == [file_path]

