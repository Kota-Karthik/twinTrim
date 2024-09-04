import os
import time
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
import click
from twinTrim.dataStructures.allFileMetadata import add_or_update_file
from twinTrim.dataStructures.fileMetadata import FileMetadata, normalStore , add_or_update_normal_file
from tqdm import tqdm

def handleAllFlag(directory):
    """Handle all duplicates automatically without asking if --all flag is set."""
    all_start_time = time.time()
    yellow = '\033[93m'
    reset = '\033[0m'
    progress_bar_format = f"{yellow}{{l_bar}}{{bar}}{{r_bar}}{{bar}}{reset}"

    # Collect all file paths to process
    all_files = [os.path.join(root, file_name) for root, _, files in os.walk(directory) for file_name in files]
    total_files = len(all_files)

    # Use ThreadPoolExecutor to handle files concurrently
    with ThreadPoolExecutor() as executor, tqdm(total=total_files, desc="Scanning files", unit="file", bar_format=progress_bar_format) as progress_bar:
        futures = {executor.submit(add_or_update_file, file_path): file_path for file_path in all_files}

        # Update progress bar as files are processed
        for future in as_completed(futures):
            progress_bar.update(1)

    click.echo(click.style("All files scanned and duplicates handled.", fg='green'))

    all_end_time = time.time()
    all_delete_time_taken = all_end_time - all_start_time
    click.echo(click.style(f"Time taken to delete all duplicate files: {all_delete_time_taken:.2f} seconds.", fg='green'))
    click.echo(click.style("All duplicates deleted!", fg='green'))


def find_duplicates(directory):
    """Find duplicate files in the given directory and store them in normalStore."""
    # First, count the total number of files to process for the progress bar
    total_files = sum([len(files) for _, _, files in os.walk(directory)])

    # Define yellow color ANSI escape code
    yellow = '\033[93m'
    reset = '\033[0m'

    # Custom progress bar format with yellow color
    progress_bar_format = f"{yellow}{{l_bar}}{{bar}}{{r_bar}}{{bar}}{reset}"

    def process_file(file_path):
        """Process an individual file, computing its hash and checking for duplicates."""
        add_or_update_normal_file(file_path)

    # Collect all file paths first
    all_files = [os.path.join(root, file_name) for root, _, files in os.walk(directory) for file_name in files]

    with ThreadPoolExecutor() as executor, tqdm(total=total_files, desc="Scanning files", unit="file", bar_format=progress_bar_format) as progress_bar:
        # Submit tasks to the executor
        futures = {executor.submit(process_file, file_path): file_path for file_path in all_files}
        
        for future in as_completed(futures):
            progress_bar.update(1)  # Update the progress bar as each file is processed

    # Gather and return duplicates from normalStore
    duplicates = []
    for _, metadata in normalStore.items():
        if len(metadata.filepaths) > 1:
            original_path = metadata.filepaths[0]
            for duplicate_path in metadata.filepaths[1:]:
                duplicates.append((original_path, duplicate_path))

    return duplicates
