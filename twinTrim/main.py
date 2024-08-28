# twinTrim/main.py
import os
import click
import time
from collections import defaultdict
from twinTrim.utils import find_duplicates


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

    duplicates_dict = defaultdict(list)
    for original, duplicate in duplicates:
        duplicates_dict[original].append(duplicate)

    # Print results
    for original, duplicates_list in duplicates_dict.items():
        click.echo(f"Original file: \"{original}\"")
        click.echo(f"Number of duplicate files found: {len(duplicates_list)}")
        click.echo("They are:")
        for idx, duplicate in enumerate(duplicates_list, 1):
            click.echo(f"{idx}) {duplicate}")
        click.echo()

    # Ask user for deletion choice
    click.confirm("Do you want to delete all duplicates permanently? (keeping the original)", abort=True)

    for original, duplicates_list in duplicates_dict.items():
        for duplicate in duplicates_list:
            try:
                os.remove(duplicate)
                click.echo(f"Deleted: {duplicate}")
            except FileNotFoundError:
                click.echo(f"File not found (skipped): {duplicate}")
            except PermissionError:
                click.echo(f"Permission denied (skipped): {duplicate}")
            except Exception as e:
                click.echo(f"Error deleting {duplicate}: {e}")

    click.echo("Duplicate files removed, keeping the original intact.")
    click.echo(f"Time taken: {time_taken:.2f} seconds.")

if __name__ == "__main__":
    cli()
