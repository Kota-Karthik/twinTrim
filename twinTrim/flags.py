import os
import click
import time
from collections import defaultdict
from twinTrim.utils import find_duplicates,handle_and_remove
from twinTrim.db import drop_all_tables, recreate_database

@click.command()
@click.argument("directory", type=click.Path(exists=True))
@click.option("--verbose", is_flag=True, help="Enable verbose output.")
@click.option("--all", is_flag=True, help="Delete duplicates automatically without asking.")
def cli(directory,delete):
    """Find and manage duplicate files in the specified DIRECTORY."""

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

    # Print results
    for original, duplicates_list in duplicates_dict.items():
        click.echo(click.style(f"Original file: \"{original}\"", fg='cyan'))
        click.echo(click.style(f"Number of duplicate files found: {len(duplicates_list)}", fg='cyan'))
        click.echo(click.style("They are:", fg='cyan'))
        for idx, duplicate in enumerate(duplicates_list, 1):
            click.echo(f"{click.style(f'{idx})', fg='magenta')} {duplicate}")
        click.echo()

    # Handle deletion based on flags
    if click.confirm(click.style("Do you want to delete all duplicates permanently? (keeping the original)", fg='red'), abort=True):
        for original, duplicates_list in duplicates_dict.items():
            for duplicate in duplicates_list:
                handle_and_remove(duplicate)
        drop_all_tables()
        recreate_database()
        click.echo(click.style("Database dropped and recreated.", fg='green'))

    click.echo(click.style("Duplicate files removed, keeping the original intact.", fg='green'))
    click.echo(click.style(f"Time taken: {time_taken:.2f} seconds.", fg='green'))
