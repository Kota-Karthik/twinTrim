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

### From PyPI

Install the latest release from PyPI using pip:

```bash
pip install twinTrim
```

You can find the project on [PyPI](https://pypi.org/project/twinTrim/).

### Setup for Development

Clone the repository and install the required dependencies using Poetry:

```bash
git clone https://github.com/Kota-Karthik/twinTrim.git
cd twinTrim
poetry install
poetry shell
```

If you haven't installed Poetry yet, you can do so by following the instructions on the [Poetry website](https://python-poetry.org/docs/#installation).