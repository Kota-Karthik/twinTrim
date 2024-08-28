# twinTrim/main.py
import os
import click
import time
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
