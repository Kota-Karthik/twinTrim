# Features

- **Duplicate Detection**: Scans directories to detect duplicate files based on file content rather than just filenames.
- **Automatic or Manual Removal**: Choose to handle duplicates automatically using the `--all` flag or manually select which files to delete.
- **Customizable Filters**: Set filters for minimum and maximum file sizes, file types, and specific filenames to exclude from the scan.
- **Multi-Threaded Processing**: Utilizes multi-threading to quickly scan and process large numbers of files concurrently.
- **Deadlock Prevention**: Implements locks to prevent deadlocks during multi-threaded operations, ensuring smooth and safe execution.
- **User-Friendly Interface**: Offers clear prompts and feedback via the command line, making the process straightforward and interactive.
