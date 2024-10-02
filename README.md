# 🔄 TwinTrim

TwinTrim is a powerful tool designed to efficiently scan and manage duplicate files across directories. It helps you keep your file system organized and save storage space by removing duplicates based on file content. 🎯

## ✨ Key Features

- 🔍 **Duplicate Detection**: Scans directories and identifies duplicate files based on their content (using MD5 hashing).
- 🤖 **Automatic or Manual Removal**: Remove duplicates automatically using the `--all` flag or manually select which files to delete.
- 🎛️ **Customizable Filters**: Control scan precision with filters for file size, type, or name exclusions.
- 🚀 **Multi-Threaded Processing**: Efficiently scans large directories by utilizing concurrent multi-threading.
- 🛡️ **Deadlock Prevention**: Ensures smooth execution by preventing deadlocks during concurrent operations.
- 💻 **User-Friendly CLI**: Offers intuitive feedback through progress bars, prompts, and clear instructions.

---

## ⚙️ How It Works

### Core Components

#### 🗂️ File Metadata Management

TwinTrim uses `AllFileMetadata` and `FileMetadata` classes to manage details like file modification time and paths. It maintains two separate dictionaries:

- **Store**: For handling duplicates.
- **NormalStore**: For managing files that aren't immediately considered duplicates.

#### 🔑 File Hashing

Each file is hashed using **MD5** to generate a unique identifier. Files with identical hashes are flagged as duplicates.

#### 🎚️ File Filtering

Through the `FileFilter` class, you can specify custom filters to refine your scan:

- **Size**: Include files within a specific range.
- **Type**: Scan only files with certain extensions (e.g., `.jpg`, `.txt`).
- **Exclusions**: Exclude files by name or pattern.

#### 🗑️ Duplicate Handling

Duplicates are identified based on file hashes. The latest version of each file (based on modification time) is kept, while older duplicates are removed.

#### 🧵 Deadlock Prevention

TwinTrim uses locking mechanisms to safely manage multi-threaded operations and avoid deadlocks.

### 🔄 Detailed Workflow

1. **Add or Update Files**: TwinTrim scans directories and either adds new files to the metadata store or updates entries when duplicates are found.
2. **Hashing and Comparison**: A unique MD5 hash is generated for each file, which is compared with existing hashes.
3. **Handling Duplicates**: Duplicate files are flagged for removal, and users can choose whether to review and confirm or allow automatic deletion.
4. **Thread-Safe Processing**: With multi-threading, TwinTrim processes multiple files concurrently, while locks ensure the system runs smoothly without resource contention.

---

## 🛠️ Usage

Run the script using the following command:

```bash
python twinTrim.py <directory> [OPTIONS]
```

### Common Options

- `--all`: Automatically delete duplicates without confirmation. 🤖
- `--min-size`: Set the minimum file size (e.g., `10kb`). 📏
- `--max-size`: Set the maximum file size (e.g., `1gb`). 📏
- `--file-type`: Filter files by type (e.g., `.jpg`, `.txt`). 🗃️
- `--exclude`: Exclude specific filenames or patterns. 🚫
- `--label-color`: Set the progress bar label color. 🎨
- `--bar-color`: Customize the progress bar color. 🌈

### 📝 Examples

**Automatic Duplicate Removal**

```bash
python twinTrim.py /path/to/directory --all
```

**Manual Review and Removal**

```bash
python twinTrim.py /path/to/directory
```

**Filtered Scan**

```bash
python twinTrim.py /path/to/directory --min-size "50kb" --max-size "500mb" --file-type "txt"
```

---

## 📥 Installation

### 🐍 Python Installation Guide

To use TwinTrim, you need Python 3.6 or later installed on your system. Follow the steps below to install Python on your machine:

#### For Windows

Download Python:
Go to the official Python website [PYTHON](https://www.python.org/downloads/) and download the latest version of Python.

Run the Installer:
Once the download is complete, open the installer. Make sure to check the box that says:

Add Python 3 to PATH before clicking the "Install Now" button.
This will ensure Python is added to your system environment variables, so you can use it from the command line.

Verify Installation: Open Command Prompt (cmd) and run the following command to verify the installation:

```bash
python --version
```

You should see the version of Python you just installed (e.g., Python 3.10.x).

#### For macOS

Download Python:
Visit the official Python website [PYTHON](https://www.python.org/downloads/) and download the latest version for macOS.

Install Python:
Open the downloaded .pkg file and follow the installation instructions.

Verify Installation:
Open the Terminal and run:

```bash
python3 --version
```

macOS comes with Python 2.x pre-installed, so you’ll need to use python3 to access the latest version.

#### For Linux

Most Linux distributions come with Python pre-installed. To install or update Python, follow these steps:

Update System Packages: Open the terminal and run:

```bash
sudo apt update
sudo apt upgrade
```

Install Python: Install Python 3.x by running:

```bash
sudo apt install python3
```

Verify Installation: Run the following command to verify:

```bash
python3 --version
```

### ⬇️ Twin Trim Installation Guide

1. Clone the repository:
   ```bash
   git clone https://github.com/Kota-Karthik/twinTrim.git
   cd twinTrim
   ```
2. Install dependencies with Poetry:
   ```bash
   poetry install
   ```
   _If you haven't installed Poetry yet click [here](https://python-poetry.org/docs/#installing-with-pipx)._

## 📦 Dependencies

- **Python 3.6+** 🐍
- `click`: For command-line interaction. 💬
- `tqdm`: For progress bars. 📊
- `concurrent.futures`: For multi-threading. 🧵
- `beaupy`: For interactive selection. ✅

## 👨‍💻 Contribution

Contributions are welcome! 🤝 Whether you have ideas for optimizing performance, refining algorithms, or improving the user interface, your input is valuable. To contribute:

1. Fork the repository.
2. Make your improvements or add new features.
3. Submit a pull request! 🚀

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/Kota-Karthik/twinTrim/blob/main/LICENSE) file for details.
