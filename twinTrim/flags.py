import os
import click
import time
from collections import defaultdict
from twinTrim.utils import handle_and_remove
from twinTrim.flagController import handleAllFlag, find_duplicates
from beaupy import select_multiple

@click.command()
@click.argument("directory", type=click.Path(exists=True))
@click.option("--all", is_flag=True, help="Delete duplicates automatically without asking.")
def cli(directory, all):
    """Find and manage duplicate files in the specified DIRECTORY."""
    if all:
        handleAllFlag(directory)
        return

    start_time = time.time()
    duplicates = find_duplicates(directory)

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
            maximal_count=len(file_options)  # Maximum number of selections allowed
        )

        # Convert the indices back to the original file paths
        files_to_delete = [duplicates_list[int(option.split(")")[0]) - 1] for option in selected_indices]

        for file_path in files_to_delete:
            handle_and_remove(file_path)

    click.echo(click.style("Selected duplicate files removed!", fg='green'))
    click.echo(click.style(f"Time taken: {time_taken:.2f} seconds.", fg='green'))

