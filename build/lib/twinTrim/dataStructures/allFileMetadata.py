import threading
import os
from typing import Dict
from twinTrim.utils import get_file_hash, handle_and_remove

class AllFileMetadata:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.file_modified_time = self.get_modification_time()
        self.__lock = threading.Lock()
    # Returns the modification time of the file.
    def get_modification_time(self):
        try:
            return os.path.getmtime(self.filepath)
        except FileNotFoundError:
            return -1
    def compare_and_replace(self, new_metadata: 'AllFileMetadata'):
        """Compares the current file's metadata with new metadata and retains the latest file."""
        if self.file_modified_time == -1:
            return
        with self.__lock:
            new_mod_time = new_metadata.get_modification_time()
            # Ignore if the new file is missing
            if new_mod_time == -1:
                return
            print("file2:", new_mod_time,"file1", self.file_modified_time)
            # Keep the most recently modified file and delete the other
            if new_mod_time > self.file_modified_time:
                handle_and_remove(self.filepath)  # Remove current file
                self.filepath = new_metadata.filepath  # Update with the new file's path
                self.file_modified_time = new_mod_time  # Update the modification time
            else:
                handle_and_remove(new_metadata.filepath)  # Remove the new file

# Store for file metadata, keyed by file hash
store: Dict[str, AllFileMetadata] = {}
store_lock = threading.Lock()
def add_or_update_file(file_path: str):
    """Adds a new file's metadata to the store or updates it if a duplicate is found."""
    file_hash = get_file_hash(file_path)  
    new_file_metadata = AllFileMetadata(file_path) 
    with store_lock:
        existing_file_metadata = store.get(file_hash)
        if existing_file_metadata is None:
            store[file_hash] = new_file_metadata 
        else:
            existing_file_metadata.compare_and_replace(new_file_metadata)
