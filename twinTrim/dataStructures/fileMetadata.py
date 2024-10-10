import threading
from typing import Dict, List
from datetime import datetime
from twinTrim.utils import get_file_hash, handle_and_remove
import pytest
from unittest.mock import patch, mock_open
from twinTrim.dataStructures.fileMetadata import add_or_update_normal_file

class FileMetadata:
    def __init__(self, filepaths: List[str]):
        self.filepaths = filepaths  

    def insert_file(self, filepath: str):
        """Inserts a new file path into the metadata if it's not already present."""
        if filepath not in self.filepaths: #this line is not necessary most probably , written by me
            self.filepaths.append(filepath)


normalStore: Dict[str, 'FileMetadata'] = {}
normalStore_lock = threading.Lock()
def test_add_or_update_file_exists():
    file_path = '/path/to/file'
    file_hash = get_file_hash(file_path)
    existing_file_metadata = normalStore.get(file_hash)
    with patch('os.path.exists', return_value=True):  
        result = add_or_update_normal_file('file_path')
        assert isinstance(result, FileMetadata)

def test_add_or_update_file_does_not_exist():
    file_path = '/path/to/file'
    with patch('os.path.exists', return_value=False):  
        with patch('builtins.open', mock_open()):  
            result = add_or_update_normal_file(file_path)
            assert result is None