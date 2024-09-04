import os

class FileFilter:
    def __init__(self):
        self.minFileSize = 0
        self.maxFileSize = float('inf')
        self.fileType = "*"
        self.fileExclude = []

    def setMinFileSize(self, size):
        self.minFileSize = size

    def setMaxFileSize(self, size):
        self.maxFileSize = size

    def setFileType(self, file_type):
        self.fileType = file_type

    def addFileExclude(self, file_name):
        self.fileExclude.append(file_name)

    def filter_files(self, file_path):
        """Check if a file meets the filter criteria."""
        if os.path.getsize(file_path) < self.minFileSize or os.path.getsize(file_path) > self.maxFileSize:
            return False
        # if self.fileType != "*" and not file_path.endswith(self.fileType):
        #     return False
        if os.path.basename(file_path) in self.fileExclude:
            return False
        return True