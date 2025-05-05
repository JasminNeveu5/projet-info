from src.analysis.pandas.TightestRace import tightestrace
# source: https://oversteer48.com/closest-f1-finishes/
theorical_tightestRace = 10

def test_tightestrace(theorical_tightestRace):
    print("non")
    assert theorical_tightestRace == tightestrace().additional_info["time_diff"]
print(test_tightestrace(theorical_tightestRace))
