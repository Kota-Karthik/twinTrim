import os
import click
import time
import logging
import inquirer
from collections import defaultdict
from twinTrim.utils import handle_and_remove, parse_size
from twinTrim.flagController import handleAllFlag, find_duplicates
from twinTrim.dataStructures.fileFilter import FileFilter

# Setting up logging configuration
logging.basicConfig(
    filename='duplicate_file_manager.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Define color constants for consistency
INFO_COLOR = 'blue'
WARNING_COLOR = 'yellow'
SUCCESS_COLOR = 'green'
ERROR_COLOR = 'red'

@click.command()
@click.argument("directory", type=click.Path(exists=True))
@click.option("--all", is_flag=True, help="Delete duplicates automatically without asking.")
@click.option("--min-size", default="0kb", type=str, help="Minimum file size in bytes.")
@click.option("--max-size", default="1gb", type=str, help="Maximum file size in bytes.")
@click.option("--file-type", default=".*", help="File type to include (e.g., .txt, .jpg).")
@click.option("--exclude", multiple=True, help="Files to exclude by name.")
@click.option("--label-color", default="yellow", type=str, help="Color of the label of progress bar.")
@click.option("--bar-color", default='#aaaaaa', type=str, help="Color of the progress bar.")
@click.option("--dry-run", is_flag=True, help="Simulate the deletion without actually removing any files.")
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
        logging.info("Deleting all duplicate files without asking.")
        handleAllFlag(directory, file_filter, label_color, bar_color, dry_run)
        return

    start_time = time.time()
    logging.info(f"Searching for duplicates in directory: {directory}")

    try:
        duplicates = find_duplicates(directory, file_filter, label_color, bar_color)
    except Exception as e:
        logging.error(f"Error finding duplicates: {str(e)}")
        click.echo(click.style("Error while finding duplicates. Check the log for details.", fg=ERROR_COLOR))
        return

    if not duplicates:
        click.echo(click.style("No duplicate files found.", fg='green'))
        logging.info("No duplicate files found.")
        return

    click.echo(click.style(f"Found {len(duplicates)} sets of duplicate files:", fg=WARNING_COLOR))
    logging.info(f"Found {len(duplicates)} set of duplicate files")

    duplicates_dict = defaultdict(list)
    for original, duplicate in duplicates:
        duplicates_dict[original].append(duplicate)

    # Process each set of duplicates
    for original, duplicates_list in duplicates_dict.items():
        click.echo(click.style(f"Original file: \"{original}\"", fg=INFO_COLOR))
        click.echo(click.style(f"Number of duplicate files found: {len(duplicates_list)}", fg=INFO_COLOR))
        logging.info(f"Original file: \"{original}\" with {len(duplicates_list)} duplicates")

        click.echo(click.style("They are:", fg=INFO_COLOR))

        # Create file options with additional information
        file_options = [
            f"{idx + 1}) {duplicate} (Size: {os.path.getsize(duplicate)} bytes)" for idx, duplicate in enumerate(duplicates_list)
        ]

        if dry_run:
            # Log and display which files would be deleted in dry-run mode
            click.echo(click.style("Dry Run Mode: These files would be deleted:", fg='yellow'))
            for option in file_options:
                click.echo(click.style(option, fg='red'))
            logging.info(f"[Dry Run] Would delete files: {file_options}")
        else:
            # If not dry run, prompt for deletion
            answers = inquirer.prompt(
                [
                    inquirer.Checkbox(
                        'files',
                        message="Select files to delete (Use space to select, enter to confirm, or ctrl+c to cancel, arrow key to navigate.)",
                        choices=file_options,
                        validate=lambda answer, current: len(answer) > 0 or "You must choose at least one file.",
                    ),
                    inquirer.Confirm(
                        'confirm',
                        message="Are you sure you want to delete the selected files?",
                        default=True
                    )
                ]
            )

            if answers and answers['confirm']:
                selected_files = answers['files']
                # Convert the selected options back to the original file paths
                files_to_delete = [duplicates_list[int(option.split(")")[0]) - 1] for option in selected_files]

                for file_path in files_to_delete:
                    handle_and_remove(file_path)
            else:
                click.echo(click.style("File deletion canceled.", fg=WARNING_COLOR))

    end_time = time.time()
    time_taken = end_time - start_time
    click.echo(click.style(f"Time taken: {time_taken:.2f} seconds.", fg=SUCCESS_COLOR))
    logging.info(f"Total time taken: {time_taken:.2f} seconds.")
