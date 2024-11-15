import os
import pytest
from unittest.mock import patch, MagicMock
from twinTrim.flagController import handleAllFlag, find_duplicates
from twinTrim.dataStructures.fileFilter import FileFilter
from twinTrim.dataStructures.fileMetadata import normalStore

# Tests for handleAllFlag
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
        (os.path.normpath('/path/to/files'), [], ['file1.txt', 'file2.txt', 'file3.txt'])
    ]
    
    # Mock file_filter to filter out some files
    mock_file_filter = MagicMock()
    mock_file_filter.filter_files.side_effect = lambda x: 'file2.txt' in x  # Only file2.txt passes the filter

    # Mock the progress bar
    mock_progress_bar.return_value.__enter__.return_value = MagicMock()

    # Call the function
    handleAllFlag(os.path.normpath('/path/to/files'), mock_file_filter, 'yellow', 'white')
    
    # Normalizing the expected file path to handle platform-specific slashes (Windows != \\)
    expected_path = os.path.normpath('/path/to/files/file2.txt')
    
    # Assertions
    mock_add_or_update_file.assert_called_once_with(expected_path)  # Only file2.txt should be processed
    mock_progress_bar.assert_called_once()  # Progress bar should still be created


@patch('os.walk')
@patch('twinTrim.flagController.add_or_update_file')
@patch('twinTrim.flagController.progress_bar_func')
def test_handle_all_flag_success(mock_progress_bar, mock_add_or_update_file, mock_os_walk):
    """Test handleAllFlag successful execution."""
    # Simulate a directory with 3 files
    mock_os_walk.return_value = [
        (os.path.normpath('/path/to/files'), [], ['file1.txt', 'file2.txt', 'file3.txt'])
    ]
    
    # Mock file_filter to allow all files
    mock_file_filter = MagicMock()
    mock_file_filter.filter_files.return_value = True

    # Mock the progress bar
    mock_progress_bar.return_value.__enter__.return_value = MagicMock()

    # Call the function
    handleAllFlag(os.path.normpath('/path/to/files'), mock_file_filter, 'yellow', 'white')

    # Assertions
    assert mock_add_or_update_file.call_count == 3  # All 3 files should be processed
    mock_progress_bar.assert_called_once()  # Progress bar should still be created


# Tests for find_duplicates
@patch('os.walk')
@patch('twinTrim.flagController.add_or_update_normal_file')
@patch('twinTrim.flagController.progress_bar_func')
def test_find_duplicates_with_duplicates(mock_progress_bar, mock_add_or_update_normal_file, mock_os_walk):
    """Test finding duplicates in a directory with multiple files."""
    # Simulate a directory with duplicate files
    mock_os_walk.return_value = [
        (os.path.normpath('/path/to/files'), [], ['file1.txt', 'file1_copy.txt', 'file2.txt'])
    ]
    
    # Mock file filter to allow all files
    mock_file_filter = MagicMock()
    mock_file_filter.filter_files.return_value = True

    # Mock the progress bar
    mock_progress_bar.return_value.__enter__.return_value = MagicMock()

    # Mock the normalStore to contain duplicates
    normalStore.clear()
    normalStore['file1_hash'] = MagicMock(filepaths=[os.path.normpath('/path/to/files/file1.txt'), os.path.normpath('/path/to/files/file1_copy.txt')])
    normalStore['file2_hash'] = MagicMock(filepaths=[os.path.normpath('/path/to/files/file2.txt')])

    # Call the function
    duplicates = find_duplicates(os.path.normpath('/path/to/files'), mock_file_filter, 'yellow', 'white')

    # Assertions
    assert len(duplicates) == 1  # Should find one duplicate pair
    assert duplicates[0][0] == os.path.normpath('/path/to/files/file1.txt')
    assert duplicates[0][1] == os.path.normpath('/path/to/files/file1_copy.txt')


@patch('os.walk')
@patch('twinTrim.flagController.progress_bar_func')
def test_find_duplicates_no_files(mock_progress_bar, mock_os_walk):
    """Test handling of a directory with no files."""
    # Mock the directory structure to return no files
    mock_os_walk.return_value = []

    # Clear normalStore to remove any leftover data from previous tests
    normalStore.clear()

    # Mock file filter
    mock_file_filter = MagicMock()

    # Mock the progress bar
    mock_progress_bar.return_value.__enter__.return_value = MagicMock()

    # Call the function
    duplicates = find_duplicates('test_directory', mock_file_filter, 'yellow', 'white')

    # Assertions
    assert duplicates == []  # Should be empty since there are no files



@patch('os.walk')
@patch('twinTrim.flagController.add_or_update_normal_file')
@patch('twinTrim.flagController.progress_bar_func')
def test_find_duplicates_with_filter(mock_progress_bar, mock_add_or_update_normal_file, mock_os_walk):
    """Test proper filtering of files using file_filter."""
    # Simulate a directory with 3 files
    mock_os_walk.return_value = [
        (os.path.normpath('/path/to/files'), [], ['file1.txt', 'file2.txt', 'file3.txt'])
    ]

    # Mock file filter to allow only 'file1.txt' and 'file2.txt'
    mock_file_filter = MagicMock()
    mock_file_filter.filter_files.side_effect = lambda f: 'file1.txt' in f or 'file2.txt' in f

    # Mock the progress bar
    mock_progress_bar.return_value.__enter__.return_value = MagicMock()

    # Mock the normalStore to contain a duplicate entry
    normalStore.clear()
    normalStore['file1_hash'] = MagicMock(filepaths=[os.path.normpath('/path/to/files/file1.txt'), os.path.normpath('/path/to/files/file2.txt')])

    # Call the function
    duplicates = find_duplicates(os.path.normpath('/path/to/files'), mock_file_filter, 'yellow', 'white')

    # Assertions
    assert len(duplicates) == 1  # Should find one duplicate pair
    assert duplicates[0][0] == os.path.normpath('/path/to/files/file1.txt')
    assert duplicates[0][1] == os.path.normpath('/path/to/files/file2.txt')
