import os

class FileFilter:
    def __init__(self):
        self.minFileSize = 0
        self.maxFileSize = 10485760
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
        # print(os.path.getsize(file_path))
        if os.path.getsize(file_path) < self.minFileSize or os.path.getsize(file_path) > self.maxFileSize:
            return False
        # if self.fileType != "*" and not file_path.endswith(self.fileType):
        #     return False
        # print(os.path.basename(file_path).strip())
        if os.path.basename(file_path.strip()) in self.fileExclude:
            return False
        return True