
import pytest
from twinTrim.dataStructures.fileFilter import FileFilter

@pytest.fixture
def file_filter():
    return FileFilter()

def test_set_max_file_size_valid_values(file_filter):
    # Test with valid file size values
    file_filter.setMaxFileSize("100kb")
    assert file_filter.maxFileSize == "100kb"
    
    file_filter.setMaxFileSize("500mb")
    assert file_filter.maxFileSize == "500mb"
    
    file_filter.setMaxFileSize("2gb")
    assert file_filter.maxFileSize == "2gb"

