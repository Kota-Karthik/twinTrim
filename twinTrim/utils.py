import hashlib
import os
from tqdm import tqdm
from twinTrim.db import create_tables, insert_file, insert_duplicate, query_duplicates

def get_file_hash(file_path):
    """Generate a hash for a given file."""
    hash_algo = hashlib.sha256()
    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            hash_algo.update(chunk)
    return hash_algo.hexdigest()

def find_duplicates(directory):
    """Find duplicate files in the given directory and store them in the database."""
    files_seen = {}

    # Create tables if they do not exist
    create_tables()

    # First, count the total number of files to process for the progress bar
    total_files = sum([len(files) for _, _, files in os.walk(directory)])
    
    # Define yellow color ANSI escape code
    yellow = '\033[93m'
    reset = '\033[0m'
    
    # Custom progress bar format with yellow color
    progress_bar_format = f"{yellow}{{l_bar}}{{bar}}{{r_bar}}{{bar}}{reset}"
    
    with tqdm(total=total_files, desc="Scanning files", unit="file", bar_format=progress_bar_format) as progress_bar:
        for root, _, files in os.walk(directory):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                file_hash = get_file_hash(file_path)

                if file_hash in files_seen:
                    original_path = files_seen[file_hash]
                    insert_file(file_path, file_hash)
                    insert_duplicate(original_path, file_path)
                else:
                    files_seen[file_hash] = file_path
                    insert_file(file_path, file_hash)

                # Update the progress bar
                progress_bar.update(1)

    return query_duplicates()
