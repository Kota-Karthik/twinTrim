import os
import click
import time
import logging
from collections import defaultdict
from twinTrim.utils import handle_and_remove, parse_size
from twinTrim.flagController import handleAllFlag, find_duplicates
from beaupy import select_multiple
from twinTrim.dataStructures.fileFilter import FileFilter

from fuzzy import find_fuzzy_duplicates

@click.command()
@click.argument("directory", type=click.Path(exists=True))
@click.option("--all", is_flag=True, help="Delete duplicates automatically without asking.")
@click.option("--min-size", default="0kb", type=str, help="Minimum file size in bytes.")
@click.option("--max-size", default="1gb", type=str, help="Maximum file size in bytes.")
@click.option("--file-type", default=".*", help="File type to include (e.g., .txt, .jpg).")
@click.option("--exclude", multiple=True, help="Files to exclude by name.")
@click.option("--label-color", default="yellow", type=str, help="Color of the label of the progress bar.")
@click.option("--bar-color", default='#aaaaaa', type=str, help="Color of the progress bar.")
@click.option("--fuzzy", is_flag=True, help="Use fuzzy matching to find duplicates.")
@click.option("--threshold", default=90, type=int, help="Similarity threshold for fuzzy matching.")
def cli(directory, all, min_size, max_size, file_type, exclude, label_color, bar_color, fuzzy, threshold):
@click.option("--dry-run", is_flag=True, help="Simulate the process without deleting files.")
def cli(directory, all, min_size, max_size, file_type, exclude, label_color, bar_color, dry_run):

    """Find and manage duplicate files in the specified DIRECTORY."""
    
    # Initialize the FileFilter object
    file_filter = FileFilter()
    file_filter.setMinFileSize(parse_size(min_size))
    file_filter.setMaxFileSize(parse_size(max_size))
    file_filter.setFileType(file_type)
    for file_name in exclude:
        file_filter.addFileExclude(file_name)

    if all:
      add-dry-run
        if dry_run:
            click.echo(click.style("Dry run mode enabled: Skipping actual deletion.", fg='yellow'))
        handleAllFlag(directory, file_filter, label_color, bar_color, dry_run=dry_run)  # Modify handleAllFlag to support dry_run
        logging.info("Deleting all duplicate files whithout asking.")
        handleAllFlag(directory, file_filter, label_color, bar_color)

        return

    start_time = time.time()
    #checking duplicates using fuzzy matchig technique
    if fuzzy:
        duplicates = find_fuzzy_duplicates(directory, file_filter, label_color, bar_color,threshold)
    
    else:
        duplicates = find_duplicates(directory, file_filter, label_color, bar_color)

    end_time = time.time()
    time_taken = end_time - start_time

    if not duplicates:
        click.echo(click.style("No duplicate files found.", fg='green'))
        logging.info("No duplicate files found.")
        return

    click.echo(click.style(f"Found {len(duplicates)} sets of duplicate files:", fg='yellow'))
    logging.info(f"Found {len(duplicates)} set of duplicate files")

    duplicates_dict = defaultdict(list)
    for original, duplicate in duplicates:
        duplicates_dict[original].append(duplicate)

    # Process each set of duplicates
    for original, duplicates_list in duplicates_dict.items():
        click.echo(click.style(f"Original file: \"{original}\"", fg='cyan'))
        click.echo(click.style(f"Number of duplicate files found: {len(duplicates_list)}", fg='cyan'))
        logging.info(f"Original file: \"{original}\" with {len(duplicates_list)} duplicates")

        click.echo(click.style("They are:", fg='cyan'))
        file_options = [f"{idx + 1}) {duplicate}" for idx, duplicate in enumerate(duplicates_list)]
        
        # Prompt user to select which files to delete
        selected_indices = select_multiple(
            file_options,  # List of files to choose from
            ticked_indices=[],         # Default indices that are selected
            maximal_count=len(file_options)  
        )

        # Convert the indices back to the original file paths
        files_to_delete = [duplicates_list[int(option.split(")")[0]) - 1] for option in selected_indices]

        for file_path in files_to_delete:
add-dry-run
            if dry_run:
                click.echo(click.style(f"[Dry Run] Would delete: {file_path}", fg='yellow'))
            else:
                handle_and_remove(file_path)

    if not dry_run:
        click.echo(click.style("Selected duplicate files removed!", fg='green'))
    else:
        click.echo(click.style("Dry run completed. No files were actually deleted.", fg='yellow'))

    click.echo(click.style(f"Time taken: {time_taken:.2f} seconds.", fg='green'))

            try:
                handle_and_remove(file_path)
                logging.info(f"Deleted duplicate file: {file_path}")
            except Exception as e:
                logging.error(f"Error deleting file {file_path}: {str(e)}")
                click.echo(click.style(f"Error deleting file: {file_path}. Check the log for details.", fg='red'))


    end_time = time.time()
    time_taken = end_time - start_time
    click.echo(click.style(f"Time taken: {time_taken:.2f} seconds.", fg='green'))
    logging.info(f"Total time taken: {time_taken:.2f} seconds.")

if __name__ == "__main__":
    cli()
 main
