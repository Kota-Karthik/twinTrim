import threading
from typing import Dict, List
from datetime import datetime
from twinTrim.utils import get_file_hash, handle_and_remove


class FileMetadata:
    def __init__(self, filepaths: List[str]):
        self.filepaths = filepaths  

    def insert_file(self, filepath: str):
        """Inserts a new file path into the metadata if it's not already present."""
        if filepath not in self.filepaths: #this line is not necessary most probably , written by me
            self.filepaths.append(filepath)


normalStore: Dict[str, 'FileMetadata'] = {}
normalStore_lock = threading.Lock()
def add_or_update_normal_file(file_path: str):
    """Adds a new file's metadata to the normalStore or updates it if a duplicate is found."""
    file_hash = get_file_hash(file_path)
    new_file_metadata = FileMetadata([file_path])

    with normalStore_lock:
        existing_file_metadata = normalStore.get(file_hash)

        if existing_file_metadata is None:
            normalStore[file_hash] = new_file_metadata
        else:
            existing_file_metadata.insert_file(file_path)