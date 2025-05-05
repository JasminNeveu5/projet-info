from src.analysis.pandas.TightestRace import tightestrace
# source: https://oversteer48.com/closest-f1-finishes/
import pytest

@pytest.fixture
def theorical_tightestRace():
    return 10

def test_tightestrace(theorical_tightestRace):
    print("non")
    assert theorical_tightestRace == tightestrace().additional_info["time_diff"]
