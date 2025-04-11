import os

import pytest
from src.Common.utils import read_csv


@pytest.fixture
def create_file():
    def _create_file(filename, content):
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        return filename

    yield _create_file
    # Cleanup to remove created files after tests
    for file in os.listdir():
        if file.startswith("test_") and file.endswith(".csv"):
            os.remove(file)


def test_read_csv_valid_file(create_file):
    filepath = create_file("test_valid.csv", "col1,col2,col3\n1,2,3\n4,5,6\n")
    expected_result = [
        {"col1": "1", "col2": "2", "col3": "3"},
        {"col1": "4", "col2": "5", "col3": "6"},
    ]
    assert read_csv(filepath) == expected_result


def test_read_csv_empty_file(create_file):
    filepath = create_file("test_empty.csv", "")
    assert read_csv(filepath) == []


def test_read_csv_file_with_only_header(create_file):
    filepath = create_file("test_only_header.csv", "col1,col2,col3\n")
    assert read_csv(filepath) == []


def test_read_csv_invalid_file_path():
    with pytest.raises(FileNotFoundError):
        read_csv("non_existent_file.csv")


@pytest.mark.parametrize(
    "content,error_type",
    [
        ("col1,col2\n1,2\n3\n", ValueError),  # Inconsistent row length
        ("col1\n1,2,3\n", ValueError),  # Too many values in a row
    ],
)
def test_read_csv_file_with_invalid_format(create_file, content, error_type):
    filepath = create_file("test_invalid.csv", content)
    with pytest.raises(error_type):
        read_csv(filepath)
