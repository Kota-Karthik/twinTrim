import os
import click
import time
from collections import defaultdict
from twinTrim.utils import handle_and_remove, parse_size
from twinTrim.flagController import handleAllFlag, find_duplicates
from beaupy import select_multiple
from twinTrim.dataStructures.fileFilter import FileFilter

@click.command()
@click.argument("directory", type=click.Path(exists=True))
@click.option("--all", is_flag=True, help="Delete duplicates automatically without asking.")
@click.option("--min-size", default="10kb", type=str, help="Minimum file size in bytes.")
@click.option("--max-size", default="1gb", type=str, help="Maximum file size in bytes.")
@click.option("--file-type", default=".*", help="File type to include (e.g., .txt, .jpg).")
@click.option("--exclude", multiple=True, help="Files to exclude by name.")
def cli(directory, all, min_size, max_size, file_type, exclude):
    """Find and manage duplicate files in the specified DIRECTORY."""

    # Initialize the FileFilter object
    file_filter = FileFilter()
    file_filter.setMinFileSize(parse_size(min_size))
    file_filter.setMaxFileSize(parse_size(max_size))
    file_filter.setFileType(file_type)
    for file_name in exclude:
        file_filter.addFileExclude(file_name)

    if all:
        handleAllFlag(directory, file_filter)
        return

    start_time = time.time()
    duplicates = find_duplicates(directory, file_filter)

    end_time = time.time()
    time_taken = end_time - start_time

    if not duplicates:
        click.echo(click.style("No duplicate files found.", fg='green'))
        click.echo(click.style(f"Time taken: {time_taken:.2f} seconds.", fg='green'))
        return

    click.echo(click.style(f"Found {len(duplicates)} sets of duplicate files:", fg='yellow'))

    duplicates_dict = defaultdict(list)
    for original, duplicate in duplicates:
        duplicates_dict[original].append(duplicate)

    # Process each set of duplicates
    for original, duplicates_list in duplicates_dict.items():
        click.echo(click.style(f"Original file: \"{original}\"", fg='cyan'))
        click.echo(click.style(f"Number of duplicate files found: {len(duplicates_list)}", fg='cyan'))
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
            handle_and_remove(file_path)

    click.echo(click.style("Selected duplicate files removed!", fg='green'))
    click.echo(click.style(f"Time taken: {time_taken:.2f} seconds.", fg='green'))
