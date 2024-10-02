import pytest
from twinTrim.dataStructures import allFileMetadata

def test_add_or_update_file_when_file_doesnt_exist(mocker):
    mockfile = "mockfile.txt"
    mocker.patch("twinTrim.dataStructures.allFileMetadata.os.path.exists", return_value=False)
    mocker.patch("twinTrim.dataStructures.allFileMetadata.get_file_hash", side_effect=FileNotFoundError)
    
    with pytest.raises(FileNotFoundError):
        allFileMetadata.add_or_update_file(mockfile)

def test_compare_and_replace_new_file_is_newer(mocker):

    file1 = "file1.txt"
    file2 = "file2.txt"

    metadata1 = allFileMetadata.AllFileMetadata(file1)
    metadata2 = allFileMetadata.AllFileMetadata(file2)


    metadata1.file_modified_time = 100
    metadata2.file_modified_time = 200
    mocker.patch("os.path.getmtime", side_effect=lambda x: {"file1.txt": 100, "file2.txt": 200}[x])

    mock_handle_and_remove = mocker.patch("twinTrim.dataStructures.allFileMetadata.handle_and_remove")

    metadata1.compare_and_replace(metadata2)
    mock_handle_and_remove.assert_called_once_with(file1)

    assert metadata1.filepath == file2
    assert metadata1.file_modified_time == 200

def test_compare_and_replace_new_file_is_older(mocker):

    file1 = "file1.txt"
    file2 = "file2.txt"

    metadata1 = allFileMetadata.AllFileMetadata(file1)
    metadata2 = allFileMetadata.AllFileMetadata(file2)


    metadata1.file_modified_time = 200
    metadata2.file_modified_time = 100
    mocker.patch("os.path.getmtime", side_effect=lambda x: {"file1.txt": 200, "file2.txt": 100}[x])

    mock_handle_and_remove = mocker.patch("twinTrim.dataStructures.allFileMetadata.handle_and_remove")
    metadata1.compare_and_replace(metadata2)
    mock_handle_and_remove.assert_called_once_with(file2)

    assert metadata1.filepath == file1
    assert metadata1.file_modified_time == 200

def test_compare_and_replace_new_file_is_missing(mocker):

    file1 = "file1.txt"
    file2 = "file2.txt"

    metadata1 = allFileMetadata.AllFileMetadata(file1)
    metadata2 = allFileMetadata.AllFileMetadata(file2)

    metadata1.file_modified_time = 200
    metadata2.file_modified_time = -1
    mocker.patch("os.path.getmtime", side_effect=lambda x: {"file1.txt": 200, "file2.txt": -1}[x])
    
    metadata1.compare_and_replace(metadata2)

    assert metadata1.filepath == file1
    assert metadata1.file_modified_time == 200

def test_compare_and_replace_old_file_is_missing(mocker):

    file1 = "file1.txt"
    file2 = "file2.txt"

    metadata1 = allFileMetadata.AllFileMetadata(file1)
    metadata2 = allFileMetadata.AllFileMetadata(file2)

    metadata1.file_modified_time = -1
    metadata2.file_modified_time = 200
    mocker.patch("os.path.getmtime", side_effect=lambda x: {"file1.txt": -1, "file2.txt": 200}[x])
    
    metadata1.compare_and_replace(metadata2)

    assert metadata1.filepath == file1
    assert metadata1.file_modified_time == -1
