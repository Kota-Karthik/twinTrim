
# TwinTrim

TwinTrim is a powerful and efficient tool designed to find and manage duplicate files across directories. It provides a streamlined way to scan files, identify duplicates based on their content, and remove them automatically or with user guidance, helping you save storage space and keep your file system organized.

## Table of Contents

- [Features](#features)
- [How It Works](#how-it-works)
	- [Core Components](#core-components)
	- [Key Functions](#key-functions)
- [Usage](#usage)
	- [Command Line Interface](#command-line-interface)
	- [Options](#options)
	- [Examples](#examples)
- [Dependencies](#dependencies)
- [Installation](#installation)
- [Contributing](#contributing)
- [Code of Conduct](#code-of-conduct)
- [License](#license)

## Features

- **Duplicate Detection**: Scans directories to detect duplicate files based on file content rather than just filenames.
- **Automatic or Manual Removal**: Choose to handle duplicates automatically using the `--all` flag or manually select which files to delete.
- **Customizable Filters**: Set filters for minimum and maximum file sizes, file types, and specific filenames to exclude from the scan.
- **Multi-Threaded Processing**: Utilizes multi-threading to quickly scan and process large numbers of files concurrently.
- **Deadlock Prevention**: Implements locks to prevent deadlocks during multi-threaded operations, ensuring smooth and safe execution.
- **User-Friendly Interface**: Offers clear prompts and feedback via the command line, making the process straightforward and interactive.

## How It Works

### Core Components

1. **File Metadata Management**: 
    - Uses `AllFileMetadata` and `FileMetadata` classes to manage file information, such as modification time and file paths.
    - Maintains metadata in two dictionaries (`store` and `normalStore`) for handling different levels of duplicate management.
  
2. **File Hashing**: 
    - Generates a unique hash for each file using MD5 to identify duplicates by content.
  
3. **File Filtering**:
    - The `FileFilter` class provides functionality to filter files based on size, type, and exclusions.
  
4. **Duplicate Handling**:
    - Duplicate files are identified by comparing their hashes.
    - Based on file modification time, the latest file is retained, and older duplicates are removed.
  
5. **Deadlock Prevention**:
    - Uses locks within multi-threaded processes to ensure that resources are accessed safely, preventing deadlocks that could otherwise halt execution.

### Key Functions

- **add_or_update_file**: Adds new files to the metadata store or updates existing entries if a duplicate is detected.
- **add_or_update_normal_file**: Similar to `add_or_update_file` but manages duplicates in a separate store.
- **handleAllFlag**: Handles duplicate removal automatically without user intervention.
- **find_duplicates**: Finds duplicate files in the specified directory and prepares them for user review or automatic handling.

## Usage

### Command Line Interface

Run the script using the following command:
```bash
python -m twinTrim.main <directory> [OPTIONS]
```

### Options

- `--all`: Automatically delete duplicates without asking for confirmation.
- `--min-size`: Specify the minimum file size to include in the scan (e.g., `10kb`).
- `--max-size`: Specify the maximum file size to include in the scan (e.g., `1gb`).
- `--file-type`: Specify the file type to include (e.g., `.txt`, `.jpg`).
- `--exclude`: Exclude specific files by name.
- `--label-color`: Set the font color of the output label of the progress bar.
- `--bar-color`: Set the color of the progress bar.

### Examples

1. **Automatic Duplicate Removal**:
    ```bash
    python -m twinTrim.main /path/to/directory --all
    ```

2. **Manual Review and Removal**:
    ```bash
    python -m twinTrim.main /path/to/directory
    ```

3. **Filtered Scan by File Size and Type**:
    ```bash
    python -m twinTrim.main /path/to/directory --min-size "50kb" --max-size "500mb" --file-type "txt"
    ```

## Dependencies

- Python 3.6+
- `click` for command-line interaction
- `tqdm` for progress bars
- `concurrent.futures` for multi-threaded processing
- `beaupy` for interactive selection

## Installation

Clone the repository and install the required dependencies using Poetry:

```bash
git clone https://github.com/Kota-Karthik/twinTrim.git
cd twinTrim
poetry install
poetry shell
```

If you haven't installed Poetry yet, you can do so by following the instructions on the [Poetry website](https://python-poetry.org/docs/#installation).

## Contributing

Contributions are welcome! Whether you have ideas for improving the internal workings of TwinTrim, such as optimizing performance or refining algorithms, or you want to enhance the user interface of the CLI tool for a better user experience, your input is valuable. Please fork the repository and submit a pull request with your improvements or new features.

Please refer to the [CONTRIBUTION_GUIEDLINES.md](./CONTRIBUTION_GUIDELINES.md) for guidelines on how to contribute.

## Code of Conduct

We value and prioritize creating a positive, welcoming, and inclusive environment for everyone involved in the **TwinTrim** project. We encourage all participants to be respectful, collaborative, and supportive of each other.

Please take a moment to review our [Code of Conduct](./CODE_OF_CONDUCT.md) to understand the expected behavior when contributing to the project.

By participating in **TwinTrim**, you agree to abide by these guidelines and help us maintain a healthy, harassment-free community.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


