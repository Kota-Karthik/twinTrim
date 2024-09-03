import hashlib
import os
from tqdm import tqdm
from twinTrim.db import create_tables, insert_files, insert_duplicates, query_duplicates
from concurrent.futures import ThreadPoolExecutor, as_completed
from queue import Queue
from threading import Thread
import click

BUF_SIZE = 65536
BATCH_SIZE = 100  # Define batch size for bulk insertion

def handle_and_remove(filepath):
    try:
        os.remove(filepath)
        click.echo(click.style(f"Deleted: {filepath}", fg='green'))
    except FileNotFoundError:
        click.echo(click.style(f"File not found (skipped): {filepath}", fg='red'))
    except PermissionError:
        click.echo(click.style(f"Permission denied (skipped): {filepath}", fg='red'))
    except Exception as e:
        click.echo(click.style(f"Error deleting {filepath}: {e}", fg='red'))                    

def get_file_hash(file_path):
    """Generate a hash for a given file."""
    hash_algo = hashlib.md5()
    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(BUF_SIZE), b""):
            hash_algo.update(chunk)
    return hash_algo.hexdigest()

def find_duplicates(directory):
    """Find duplicate files in the given directory and store them in the database."""
    files_seen = {}
    db_queue = Queue()

    # Create tables if they do not exist
    create_tables()

    # First, count the total number of files to process for the progress bar
    total_files = sum([len(files) for _, _, files in os.walk(directory)])

    # Define yellow color ANSI escape code
    yellow = '\033[93m'
    reset = '\033[0m'

    # Custom progress bar format with yellow color
    progress_bar_format = f"{yellow}{{l_bar}}{{bar}}{{r_bar}}{{bar}}{reset}"

    def process_file(file_path):
        """Process an individual file, computing its hash and checking for duplicates."""
        file_hash = get_file_hash(file_path)

        if file_hash in files_seen:
            original_path = files_seen[file_hash]
            db_queue.put(('duplicate', original_path, file_path, file_hash))
        else:
            files_seen[file_hash] = file_path
            db_queue.put(('file', file_path, file_hash))

    def db_worker():
        """Process items in the queue and handle database operations in batches."""
        file_batch = []  # Collect data in batches for files
        duplicate_batch = []  # Collect data in batches for duplicates

        while True:
            item = db_queue.get()
            if item is None:  # Stop the worker if None is received
                break
            
            if item[0] == 'duplicate':
                _, original_path, duplicate_path, file_hash = item
                file_batch.append((duplicate_path, file_hash))
                duplicate_batch.append((original_path, duplicate_path))
            elif item[0] == 'file':
                _, file_path, file_hash = item
                file_batch.append((file_path, file_hash))
            
            if len(file_batch) >= BATCH_SIZE:
                insert_files(file_batch)
                file_batch.clear()
            
            if len(duplicate_batch) >= BATCH_SIZE:
                insert_duplicates(duplicate_batch)
                duplicate_batch.clear()

            db_queue.task_done()  # Mark the queue task as done
        
        # Insert any remaining items in the batches
        if file_batch:
            insert_files(file_batch)
        if duplicate_batch:
            insert_duplicates(duplicate_batch)

    # Start the database worker thread
    db_thread = Thread(target=db_worker)
    db_thread.start()

    # Collect all file paths first
    all_files = [os.path.join(root, file_name) for root, _, files in os.walk(directory) for file_name in files]

    with ThreadPoolExecutor() as executor, tqdm(total=total_files, desc="Scanning files", unit="file", bar_format=progress_bar_format) as progress_bar:
        # Submit tasks to the executor
        futures = {executor.submit(process_file, file_path): file_path for file_path in all_files}
        
        for future in as_completed(futures):
            progress_bar.update(1)  # Update the progress bar as each file is processed

    # Wait for all tasks to be completed
    db_queue.join()  # Wait until all items in the queue have been processed

    # Stop the database worker thread
    db_queue.put(None)  # Send the stop signal to the worker
    db_thread.join()

    return query_duplicates()




