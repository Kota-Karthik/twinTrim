import pytest
from twinTrim.utils import parse_size  # Adjust based on actual import path

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


    # If you decide to raise exceptions for invalid formats, uncomment this part:
    # with pytest.raises(ValueError):
    #     parse_size("abc")
    # with pytest.raises(ValueError):
    #     parse_size("10x")
    # with pytest.raises(ValueError):
    #     parse_size("100.5xyz")