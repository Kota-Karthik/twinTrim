import pytest
import os
from pathlib import Path
from unittest.mock import patch, MagicMock, mock_open
from twinTrim.flagController import handleAllFlag
from twinTrim.dataStructures.fileFilter import FileFilter
from twinTrim.flagController import find_duplicates

@patch('os.walk')
@patch('twinTrim.flagController.add_or_update_file')
@patch('twinTrim.flagController.progress_bar_func')
def test_handle_all_flag_no_files(mock_progress_bar, mock_add_or_update_file, mock_os_walk):
    """Test handleAllFlag when directory has no files."""
    # Mock the directory structure to return no files
    mock_os_walk.return_value = []

    # Mock the progress bar to avoid actual printing
    mock_progress_bar.return_value.__enter__.return_value = MagicMock()

    # Call the function with mock parameters
    handleAllFlag('test_directory', MagicMock(), 'yellow', 'white')

    # Assertions
    mock_add_or_update_file.assert_not_called()  # Since there are no files
    mock_progress_bar.assert_called_once()  # Progress bar should still be created


@patch('os.walk')
@patch('twinTrim.flagController.add_or_update_file')
@patch('twinTrim.flagController.progress_bar_func')
def test_handle_all_flag_filtered_files(mock_progress_bar, mock_add_or_update_file, mock_os_walk):
    """Test handleAllFlag with files that pass the filter."""
    # Simulate a directory with 3 files
    mock_os_walk.return_value = [
        ('/path/to/files', [], ['file1.txt', 'file2.txt', 'file3.txt'])
    ]
    
    # Mock file_filter to filter out some files
    mock_file_filter = MagicMock()
    mock_file_filter.filter_files.side_effect = lambda x: 'file2.txt' in x  # Only file2.txt passes the filter

    # Mock the progress bar
    mock_progress_bar.return_value.__enter__.return_value = MagicMock()

    # Call the function
    handleAllFlag('/path/to/files', mock_file_filter, 'yellow', 'white')

    # Assertions
    mock_add_or_update_file.assert_called_once_with('/path/to/files/file2.txt')  # Only file2.txt should be processed
    mock_progress_bar.assert_called_once()  # Progress bar should still be created


@patch('os.walk')
@patch('twinTrim.flagController.add_or_update_file')
@patch('twinTrim.flagController.progress_bar_func')
def test_handle_all_flag_success(mock_progress_bar, mock_add_or_update_file, mock_os_walk):
    """Test handleAllFlag successful execution."""
    # Simulate a directory with 3 files
    mock_os_walk.return_value = [
        ('/path/to/files', [], ['file1.txt', 'file2.txt', 'file3.txt'])
    ]
    
    # Mock file_filter to allow all files
    mock_file_filter = MagicMock()
    mock_file_filter.filter_files.return_value = True

    # Mock the progress bar
    mock_progress_bar.return_value.__enter__.return_value = MagicMock()

    # Call the function
    handleAllFlag('/path/to/files', mock_file_filter, 'yellow', 'white')

    # Assertions
    assert mock_add_or_update_file.call_count == 3  # All 3 files should be processed
    mock_progress_bar.assert_called_once()  # Progress bar should still be created


def count_files(directory):
    if not isinstance(directory, (str, Path)):
        raise TypeError("Directory path must be a string or Path object")
        
    if not os.path.exists(directory):
        raise FileNotFoundError(f"Directory '{directory}' does not exist")
        
    if not os.path.isdir(directory):
        raise NotADirectoryError(f"'{directory}' is not a directory")
    
    total_files = 0
    for root, _, files in os.walk(directory):
        total_files += len(files)
    
    return total_files

def test_count_files_empty_directory(tmp_path):
    assert count_files(str(tmp_path)) == 0

def test_count_files_single_file(tmp_path):
    file_path = tmp_path / "test.txt"
    file_path.write_text("test content")
    assert count_files(str(tmp_path)) == 1

def test_count_files_multiple_files(tmp_path):
    for i in range(3):
        file_path = tmp_path / f"test{i}.txt"
        file_path.write_text(f"content {i}")
    
    assert count_files(str(tmp_path)) == 3

def test_count_files_with_subdirectories(tmp_path):
    (tmp_path / "file1.txt").write_text("content")
    (tmp_path / "file2.txt").write_text("content")
    
    subdir = tmp_path / "subdir"
    subdir.mkdir()
    (subdir / "file3.txt").write_text("content")
    (subdir / "file4.txt").write_text("content")
    
    assert count_files(str(tmp_path)) == 4

def test_count_files_nonexistent_directory():
    with pytest.raises(FileNotFoundError):
        count_files("/nonexistent/directory")

def test_count_files_invalid_input():
    with pytest.raises(TypeError):
        count_files(123)

def test_count_files_file_as_input(tmp_path):
    file_path = tmp_path / "test.txt"
    file_path.write_text("test content")
    
    with pytest.raises(NotADirectoryError):
        count_files(str(file_path))

def test_count_files_with_hidden_files(tmp_path):
    (tmp_path / "visible.txt").write_text("content")
    (tmp_path / ".hidden").write_text("content")
    
    assert count_files(str(tmp_path)) == 2