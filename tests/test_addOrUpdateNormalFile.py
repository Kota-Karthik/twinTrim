import pytest
from twinTrim.dataStructures.fileMetadata import add_or_update_normal_file, normalStore, FileMetadata
from unittest.mock import patch

@pytest.fixture(autouse=True)
def clear_normal_store():
    normalStore.clear()

@patch('twinTrim.dataStructures.fileMetadata.get_file_hash')
def test_add_new_file_to_empty_store(mock_get_file_hash):
    mock_get_file_hash.return_value = 'hash1'
    
    add_or_update_normal_file('file1.txt')
    
    assert len(normalStore) == 1
    assert 'hash1' in normalStore
    assert normalStore['hash1'].filepaths == ['file1.txt']

@patch('twinTrim.dataStructures.fileMetadata.get_file_hash')
def test_update_existing_file_metadata(mock_get_file_hash):
    mock_get_file_hash.return_value = 'hash1'
    
    add_or_update_normal_file('file1.txt')
    add_or_update_normal_file('file2.txt')
    
    assert len(normalStore) == 1
    assert 'hash1' in normalStore
    assert set(normalStore['hash1'].filepaths) == {'file1.txt', 'file2.txt'}

@patch('twinTrim.dataStructures.fileMetadata.get_file_hash')
def test_no_duplicate_insertion_in_metadata(mock_get_file_hash):
    mock_get_file_hash.return_value = 'hash1'
    
    add_or_update_normal_file('file1.txt')
    add_or_update_normal_file('file1.txt')
    
    assert len(normalStore) == 1
    assert 'hash1' in normalStore
    assert normalStore['hash1'].filepaths == ['file1.txt']

@patch('twinTrim.dataStructures.fileMetadata.get_file_hash')
def test_multiple_files_different_hashes(mock_get_file_hash):
    mock_get_file_hash.side_effect = ['hash1', 'hash2', 'hash3']
    
    add_or_update_normal_file('file1.txt')
    add_or_update_normal_file('file2.txt')
    add_or_update_normal_file('file3.txt')
    
    assert len(normalStore) == 3
    assert 'hash1' in normalStore and normalStore['hash1'].filepaths == ['file1.txt']
    assert 'hash2' in normalStore and normalStore['hash2'].filepaths == ['file2.txt']
    assert 'hash3' in normalStore and normalStore['hash3'].filepaths == ['file3.txt']
