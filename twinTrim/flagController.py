import os
import time
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
import click
from twinTrim.dataStructures.allFileMetadata import add_or_update_file
from twinTrim.dataStructures.fileMetadata import FileMetadata, normalStore , add_or_update_normal_file
from tqdm import tqdm

#bar function to be used by scanner thread pools
progress_bar_format = "{desc}: {n_fmt}/{total_fmt} | ETA={remaining} | {rate_fmt} {bar} {percentage:.3f}%"
"""adaptive progress bar, returns tqdm object"""
def progress_bar_func(bar_desc, total, unit='file',color="yellow", bar_color='white'):
    try: #default to yellow
        bar_desc_obj = click.style(bar_desc, fg=color, bold=True) # set to bold by default
    except:
        print(f"Warning, invalid ColorType: {color} falling back to default yellow.")
        bar_desc_obj = click.style(bar_desc, fg='yellow', bold=True)
    return tqdm(total=total, desc=bar_desc_obj, unit=unit, bar_format= progress_bar_format, colour=bar_color)

def handleAllFlag(directory,file_filter,pb_color,bar_color):
    """Handle all duplicates automatically without asking if --all flag is set."""
    all_start_time = time.time()

    # Collect all file paths to process
    all_files = [os.path.join(root, file_name) for root, _, files in os.walk(directory) for file_name in files]
    all_files = [f for f in all_files if file_filter.filter_files(f)] 
    total_files = len(all_files)

    # Use ThreadPoolExecutor to handle files concurrently
    with ThreadPoolExecutor() as executor, progress_bar_func("Scanning", total_files, color=pb_color, bar_color=bar_color) as progress_bar:
        futures = {executor.submit(add_or_update_file, file_path): file_path for file_path in all_files}

        # Update progress bar as files are processed
        for future in as_completed(futures):
            try:
                future.result()  # Ensures exception handling for each future
            except Exception as e:
                click.echo(click.style(f"Error processing file {futures[future]}: {str(e)}", fg='red'))
            progress_bar.update(1)

    click.echo(click.style("All files scanned and duplicates handled.", fg='green'))

    all_end_time = time.time()
    all_delete_time_taken = all_end_time - all_start_time
    click.echo(click.style(f"Time taken to delete all duplicate files: {all_delete_time_taken:.2f} seconds.", fg='green'))
    click.echo(click.style("All duplicates deleted!", fg='green'))


def find_duplicates(directory, file_filter, pb_color, bar_color):
    """Find duplicate files in the given directory and store them in normalStore."""
    # Collect all file paths first and apply filters
    start_time=time.time()
    all_files = [os.path.join(root, file_name) for root, _, files in os.walk(directory) for file_name in files]
    all_files = [f for f in all_files if file_filter.filter_files(f)]  # Apply filters

    # Calculate the total number of files and ensure it is finite
    total_files = len(all_files)

    def process_file(file_path):
        add_or_update_normal_file(file_path)

    with ThreadPoolExecutor() as executor, progress_bar_func("Hashing", total_files, color=pb_color, bar_color=bar_color) as progress_bar:
        # Submit tasks to the executor
        futures = {executor.submit(process_file, file_path): file_path for file_path in all_files}
        
        for future in as_completed(futures):
            try:
                future.result()  # Ensures exception handling for each future
            except Exception as e:
                click.echo(click.style(f"Error processing file {futures[future]}: {str(e)}", fg='red'))
            progress_bar.update(1)

    end_time=time.time()
    click.echo(click.style(f"Time taken to find all duplicate files: {end_time-start_time:.2f} seconds.", fg='green'))
    duplicates = []
    for _, metadata in normalStore.items():
        if len(metadata.filepaths) > 1:
            original_path = metadata.filepaths[0]
            for duplicate_path in metadata.filepaths[1:]:
                duplicates.append((original_path, duplicate_path))

    return duplicates
