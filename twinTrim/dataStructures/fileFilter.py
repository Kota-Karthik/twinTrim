import os
import re

class FileFilter:
    def __init__(self):
        self.minFileSize = "0kb"
        self.maxFileSize = "1gb"
        self.fileType = r"^.+\.*$" 
        self.fileExclude = []

    def setMinFileSize(self, size):
     if isinstance(size, (int, float)) and size > 0:
        self.minFileSize = size
     elif isinstance(size, str):
        # Optionally add regex to validate file size strings like '10kb', '500mb'
        self.minFileSize = size
     else:
        raise ValueError("Invalid size: must be a positive number or a valid size string.")


    def setMaxFileSize(self, size):
        self.maxFileSize = size

    def setFileType(self, file_type):
        self.fileType = rf"^.+\.{file_type}$"  

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
    def test_setMinFileSize_valid_integer():
     file_filter = FileFilter()
     file_filter.setMinFileSize(1024)
     assert file_filter.minFileSize == 1024

    def test_setMinFileSize_valid_string():
     file_filter = FileFilter()
     file_filter.setMinFileSize("10kb")
     assert file_filter.minFileSize == "10kb"
 
    def test_setMinFileSize_negative_number():
     file_filter = FileFilter()
     with pytest.raises(ValueError):
      file_filter.setMinFileSize(-1024)

    def test_setMinFileSize_zero():
     file_filter = FileFilter()
     with pytest.raises(ValueError):
        file_filter.setMinFileSize(0)
  

