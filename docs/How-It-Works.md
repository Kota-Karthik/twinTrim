# How It Works

## Core Components

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

## Key Functions

- **add_or_update_file**: Adds new files to the metadata store or updates existing entries if a duplicate is detected.
- **add_or_update_normal_file**: Similar to `add_or_update_file` but manages duplicates in a separate store.
- **handleAllFlag**: Handles duplicate removal automatically without user intervention.
- **find_duplicates**: Finds duplicate files in the specified directory and prepares them for user review or automatic handling.
