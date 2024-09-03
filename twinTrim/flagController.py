import os
import time
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
import click
from twinTrim.dataStructures import AllFileMetadata, store, add_or_update_file, store_lock

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
