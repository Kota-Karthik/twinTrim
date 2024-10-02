import os
import re

class FileFilter:
    def __init__(self):
        self.minFileSize = "0kb"
        self.maxFileSize = "1gb"
        self.fileType = r"^.+\.*$" 
        self.fileExclude = []



    def addFileExclude(self, file_name):
        self.fileExclude.append(file_name)

    def filter_files(self, file_path):
        """Check if a file meets the filter criteria."""
        if os.path.getsize(file_path) < self.minFileSize or os.path.getsize(file_path) > self.maxFileSize:
            return False
        if not re.match(self.fileType, os.path.basename(file_path)):  
            return False
        if os.path.basename(file_path).strip() in self.fileExclude:
            return False
        return True
