import threading
from typing import Dict, List
from datetime import datetime
from twinTrim.utils import get_file_hash, handle_and_remove

class FileMetadata:
    def __init__(self, filepaths: List[str]):
        self.filepaths = filepaths  # List of file paths with the same hash
        self.duplicate_count = len(filepaths)  # Count of duplicates
        self.timestamp = datetime.now()  # Timestamp when the first file was added

    def insert_file(self, filepath: str):
        """Inserts a new file path into the metadata and updates duplicate count."""
        if filepath not in self.filepaths:  # Avoid duplicates
            self.filepaths.append(filepath)
            self.duplicate_count += 1
            print(f"File {filepath} added. Duplicate count: {self.duplicate_count}")
        else:
            print(f"File {filepath} is already present.")

normalStore: Dict[str, 'FileMetadata'] = {}
normalStore_lock = threading.Lock()

def add_or_update_normal_file(file_path: str):
    """Adds a new file's metadata to the normalStore or updates it if a duplicate is found."""
    file_hash = get_file_hash(file_path)
    new_file_metadata = FileMetadata([file_path])  # New metadata with the file

    with normalStore_lock:  # Ensure thread safety
        existing_file_metadata = normalStore.get(file_hash)

        if existing_file_metadata is None:
            normalStore[file_hash] = new_file_metadata
            print(f"File {file_path} added with hash {file_hash}. Timestamp: {new_file_metadata.timestamp}")
        else:
            existing_file_metadata.insert_file(file_path)

def get_file_info(file_hash: str):
    """Returns metadata for a file hash."""
    with normalStore_lock:
        return normalStore.get(file_hash)

def remove_file(file_path: str):
    """Removes a file from the store."""
    file_hash = get_file_hash(file_path)
    
    with normalStore_lock:
        file_metadata = normalStore.get(file_hash)
        if file_metadata and file_path in file_metadata.filepaths:
            file_metadata.filepaths.remove(file_path)
            file_metadata.duplicate_count -= 1
            if file_metadata.duplicate_count == 0:
                del normalStore[file_hash]  # Remove metadata if no files are left
            print(f"File {file_path} removed.")
        else:
            print(f"File {file_path} not found in store.")

# Example usage of the functions:
# add_or_update_normal_file('/path/to/file1')
# add_or_update_normal_file('/path/to/file2')
# remove_file('/path/to/file1')
