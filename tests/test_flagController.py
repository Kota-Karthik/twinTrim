import pytest
from unittest.mock import patch, MagicMock
from twinTrim.flagController import handleAllFlag
from twinTrim.dataStructures.fileFilter import FileFilter

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
