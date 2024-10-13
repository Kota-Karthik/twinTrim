import threading
import os
import logging
from typing import Dict
from twinTrim.utils import get_file_hash, handle_and_remove

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AllFileMetadata:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.file_modified_time = self.get_modification_time()
        self.__lock = threading.Lock()

    def get_modification_time(self) -> float:
        """Returns the modification time of the file. If the file doesn't exist, returns -1."""
        try:
            return os.path.getmtime(self.filepath)
        except FileNotFoundError:
            logging.error(f"File not found: {self.filepath}")
            return -1

    def compare_and_replace(self, new_metadata: 'AllFileMetadata') -> None:
        """Compares the current file's metadata with new metadata and retains the latest file."""
        if self.file_modified_time == -1:
            return
        with self.__lock:
            new_mod_time = new_metadata.get_modification_time()
            if new_mod_time == -1:
                return
            logging.info(f"Comparing files - New: {new_mod_time}, Existing: {self.file_modified_time}")
            if new_mod_time > self.file_modified_time:
                handle_and_remove(self.filepath)
                self.filepath = new_metadata.filepath
                self.file_modified_time = new_mod_time
            else:
                handle_and_remove(new_metadata.filepath)

# Store for file metadata, keyed by file hash
store: Dict[str, AllFileMetadata] = {}
store_lock = threading.Lock()

def add_or_update_file(file_path: str) -> None:
    """Adds a new file's metadata to the store or updates it if a duplicate is found."""
    file_hash = get_file_hash(file_path)
    new_file_metadata = AllFileMetadata(file_path)
    
    with store_lock:
        existing_file_metadata = store.get(file_hash)
        if existing_file_metadata is None:
            store[file_hash] = new_file_metadata
            logging.info(f"Added new file to store: {file_path}")
        else:
            existing_file_metadata.compare_and_replace(new_file_metadata)
