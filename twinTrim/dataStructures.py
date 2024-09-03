import threading
import os
from typing import Dict
from .utils import get_file_hash,handle_and_remove

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
        if self.file_modified_time == -1:
            return
        with self.__lock:
            new_mod_time = new_metadata.get_modification_time()

            if new_mod_time == -1:
                return
            
            if new_mod_time > self.file_modified_time:
                handle_and_remove(self.filepath)
                self.filepath = new_metadata.filepath
            else:
                handle_and_remove(new_metadata.filepath)


store: Dict[str, AllFileMetadata] = {}
store_lock=threading.Lock()
def add_or_update_file(file_path: str):
    file_hash = get_file_hash(file_path)
    new_file_metadata = AllFileMetadata(file_path)
    with store_lock:
        existing_file_metadata = store.get(file_hash)

        if existing_file_metadata is None:
            store[file_hash] = new_file_metadata
        else:
            existing_file_metadata.compare_and_replace(new_file_metadata)

    