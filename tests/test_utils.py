import os
import pytest
import tempfile 
import unittest
from unittest import mock
from twinTrim.utils import parse_size, get_file_hash,handle_and_remove  # Adjust based on actual import path
import click
import io
import sys
# Tests for parse_size function
class TestHandleAndRemove(unittest.TestCase):
    
    def setUp(self):
        # Create a temporary file to test deletion
        self.temp_file = tempfile.NamedTemporaryFile(delete=True)
        self.temp_file_path = self.temp_file.name  # Get the file path

    def tearDown(self):
        # Cleanup: Make sure the temp file is removed
        try:
            os.remove(self.temp_file_path)
        except Exception:
            pass  # If it doesn't exist, ignore the error

    def test_handle_and_remove_success(self):
        # Test successful file deletion
        result = handle_and_remove(self.temp_file_path)
        self.assertFalse(os.path.exists(self.temp_file_path))  # File should not exist anymore

    @mock.patch("os.remove")
    
    def test_handle_and_remove_file_not_found(self, mock_remove):
    # Simulate FileNotFoundError
        mock_remove.side_effect = FileNotFoundError
        with mock.patch('sys.stdout', new=io.StringIO()) as fake_out:
            handle_and_remove("non_existent_file.txt")
            output = fake_out.getvalue()  # Capture the printed output
            self.assertIn("File not found (skipped): non_existent_file.txt", output)

    @mock.patch("os.remove")
    def test_handle_and_remove_permission_error(self, mock_remove):
    # Simulate PermissionError
        mock_remove.side_effect = PermissionError
        with mock.patch('sys.stdout', new=io.StringIO()) as fake_out:
            handle_and_remove(self.temp_file_path)  # Using temp file to ensure we have a real file
            output = fake_out.getvalue()  # Capture the printed output
            self.assertIn("Permission denied (skipped): {}".format(self.temp_file_path), output)

if __name__ == "__main__":
    unittest.main()

def test_parse_size_valid():
    # Test valid size strings
    assert parse_size("10kb") == 10 * 1024  # 10 * 1024 bytes = 10240
    assert parse_size("1mb") == 1 * 1024 * 1024  # 1 * 1024 * 1024 bytes = 1048576
    assert parse_size("1.5gb") == int(1.5 * 1024 * 1024 * 1024)  # 1610612736 bytes
    assert parse_size("0kb") == 0  # Edge case: 0kb should be 0
    assert parse_size("0mb") == 0  # Edge case: 0mb should be 0
    assert parse_size("0gb") == 0  # Edge case: 0gb should be 0

def test_parse_size_invalid():
    # Test invalid size strings
    assert parse_size("abc") == 0  # Non-numeric input should return 0
    assert parse_size("10x") == 0
    assert parse_size("100.5xyz") == 0

    # Uncomment to raise exceptions for invalid formats:
    # with pytest.raises(ValueError):
    #     parse_size("abc")
    # with pytest.raises(ValueError):
    #     parse_size("10x")
    # with pytest.raises(ValueError):
    #     parse_size("100.5xyz")

# Fixture for creating a temporary file with 'hello' content
@pytest.fixture
def create_temp_file():
    """Fixture to create a temporary file with known content."""
    with tempfile.NamedTemporaryFile(delete=False, mode='w+') as tmp_file:
        tmp_file.write("hello")  # Write 'hello' to the file for hashing
        tmp_file.flush()  # Flush to ensure the content is written
        yield tmp_file.name  # Provide the name for the test
    os.remove(tmp_file.name)  # Cleanup after test

@pytest.fixture
def create_empty_file():
    """Fixture to create an empty temporary file."""
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        yield tmp_file.name  # Provide the name for the test
    os.remove(tmp_file.name)  # Cleanup after test

# Tests for get_file_hash function
def test_get_file_hash_regular_file(create_temp_file):
    """Test hashing for a regular file with known content."""
    hash_value = get_file_hash(create_temp_file)
    expected_hash = "5d41402abc4b2a76b9719d911017c592"  # MD5 hash for 'hello'
    assert hash_value == expected_hash

def test_get_file_hash_empty_file(create_empty_file):
    """Test hashing for an empty file."""
    hash_value = get_file_hash(create_empty_file)
    expected_hash = "d41d8cd98f00b204e9800998ecf8427e"  # MD5 hash for an empty file
    assert hash_value == expected_hash

def test_get_file_hash_non_existent_file():
    """Test handling of non-existent file."""
    with pytest.raises(FileNotFoundError):
        get_file_hash("non_existent_file.txt")
