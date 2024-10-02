import pytest
from twinTrim.dataStructures import allFileMetadata

def test_add_or_update_file_when_file_doesnt_exist(mocker):
    mockfile = "mockfile.txt"
    mocker.patch("twinTrim.dataStructures.allFileMetadata.os.path.exists", return_value=False)
    mocker.patch("twinTrim.dataStructures.allFileMetadata.get_file_hash", side_effect=FileNotFoundError)
    
    with pytest.raises(FileNotFoundError):
        allFileMetadata.add_or_update_file(mockfile)
