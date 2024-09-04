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

    