# twinTrim/main.py

import os
import hashlib
import click
from tqdm import tqdm
import time

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

@click.command()
@click.argument("directory", type=click.Path(exists=True))
def cli(directory):
    """Find and manage duplicate files in the specified DIRECTORY."""

    start_time = time.time()  # Start timing the operation

    duplicates = find_duplicates(directory)

    end_time = time.time()  # End timing the operation
    time_taken = end_time - start_time

    if not duplicates:
        click.echo("No duplicate files found.")
        click.echo(f"Time taken: {time_taken:.2f} seconds.")
        return

    click.echo(f"Found {len(duplicates)} sets of duplicate files:")

    for i, (original, duplicate) in enumerate(duplicates, 1):
        click.echo(f"{i}.")
        click.echo(f"Original: {original}")
        click.echo(f"Duplicate: {duplicate}")

    # Ask user for deletion choice
    click.confirm("Do you want to delete all duplicates permanently? (keeping the original)", abort=True)

    for _, duplicate in duplicates:
        os.remove(duplicate)
        click.echo(f"Deleted: {duplicate}")

    click.echo("Duplicate files removed, keeping the original intact.")
    click.echo(f"Time taken: {time_taken:.2f} seconds.")

if __name__ == "__main__":
    cli()
