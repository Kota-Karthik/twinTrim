import os
import hashlib
from concurrent.futures import ThreadPoolExecutor, as_completed
import click

BUF_SIZE = 131072

def handle_and_remove(filepath):
    try:
        os.remove(filepath)
        click.echo(click.style(f"Deleted: {filepath}", fg='green'))
    except FileNotFoundError:
        click.echo(click.style(f"File not found (skipped): {filepath}", fg='red'))
    except PermissionError:
        click.echo(click.style(f"Permission denied (skipped): {filepath}", fg='red'))
    except Exception as e:
        click.echo(click.style(f"Error deleting {filepath}: {e}", fg='red'))                    

def get_file_hash(file_path):
    """Generate a hash for a given file."""
    hash_algo = hashlib.md5()
    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(BUF_SIZE), b""):
            hash_algo.update(chunk)
    return hash_algo.hexdigest()

def parse_size(size_str):
    size_str = size_str.lower()
    try:
        if size_str.endswith('kb'):
            return int(float(size_str[:-2]) * 1024)
        elif size_str.endswith('mb'):
            return int(float(size_str[:-2]) * 1024 * 1024)
        elif size_str.endswith('gb'):
            return int(float(size_str[:-2]) * 1024 * 1024 * 1024)
        else:
            # Attempt to convert size_str to an integer
            return int(size_str)  # This can also be modified to handle sizes without suffix
    except ValueError:
        # If conversion fails, return 0 for invalid formats
        return 0
