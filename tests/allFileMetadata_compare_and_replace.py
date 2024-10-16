import os
import pytest
from twinTrim.dataStructures.allFileMetadata import AllFileMetadata, handle_and_remove

# Test for compare_and_replace method
class TestAllFileMetadata:

    def test_compare_and_replace_correct_file_removed(self, tmp_path):
        # Create two temporary files
        file1 = tmp_path / "file1.txt"
        file2 = tmp_path / "file2.txt"
        file1.write_text("File 1")
        file2.write_text("File 2")

        # Set modification times (file2 is newer)
        os.utime(file1, (1, 1))
        os.utime(file2, (2, 2))

        # Initialize AllFileMetadata instances
        metadata1 = AllFileMetadata(str(file1))
        metadata2 = AllFileMetadata(str(file2))

        # Call the method
        metadata1.compare_and_replace(metadata2)

        # Assert the correct file is removed
        assert file1.exists()  # file1 should still exist
        assert not file2.exists()  # file2 should be removed

    def test_compare_and_replace_no_file_removed_if_one_does_not_exist(self, tmp_path):
        # Create one temporary file
        file1 = tmp_path / "file1.txt"
        file1.write_text("File 1")

        # Non-existent file path
        file2 = tmp_path / "file2.txt"  # This file will not be created

        # Initialize AllFileMetadata instances
        metadata1 = AllFileMetadata(str(file1))
        metadata2 = AllFileMetadata(str(file2))  # This will simulate a missing file

        # Call the method
        metadata1.compare_and_replace(metadata2)

        # Assert no file is removed
        assert file1.exists()  # file1 should still exist

    def test_compare_and_replace_no_file_removed_if_both_do_not_exist(self, tmp_path):
        # Non-existent file paths
        file1 = tmp_path / "file1.txt"  # Simulating a non-existent file
        file2 = tmp_path / "file2.txt"  # Another non-existent file

        # Initialize AllFileMetadata instances with non-existent paths
        metadata1 = AllFileMetadata(str(file1))
        metadata2 = AllFileMetadata(str(file2))

        # Call the method
        metadata1.compare_and_replace(metadata2)

        # Assert no file is removed
        assert not file1.exists()  # file1 does not exist
        assert not file2.exists()  # file2 does not exist