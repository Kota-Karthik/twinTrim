import hashlib
import os
from tqdm import tqdm

def get_file_hash(file_path):
    """Generate a hash for a given file."""
    hash_algo = hashlib.sha256()
    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            hash_algo.update(chunk)
    return hash_algo.hexdigest()


def find_duplicates(directory):
    """Find duplicate files in the given directory."""
    files_seen = {}
    duplicates = []

    # Count the total number of files for the progress bar
    total_files = sum(len(files) for _, _, files in os.walk(directory))

    # Using tqdm for the progress bar
    with tqdm(total=total_files, desc="Scanning Files", unit="file") as pbar:
        for root, _, files in os.walk(directory):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                file_hash = get_file_hash(file_path)

                if file_hash in files_seen:
                    duplicates.append((files_seen[file_hash], file_path))
                else:
                    files_seen[file_hash] = file_path

                pbar.update(1)  # Update the progress bar for each file processed

    return duplicates