from options.config import DATA_DIR
from src.Model.Race import Race
import pandas as pd


def tightestrace():
    """
    Determines the race with the tightest finishing time difference between the
    first and second place finishers. It calculates the time difference
    between the first two positions for every race, identifies the race with
    the smallest recorded time difference, and returns the corresponding
    race details as a Race object.

    :return: An instance of the `Race` class containing the details of the
        race with the tightest finishing time difference. This includes the
        name of the race, the year it occurred, the date of the race, and the
        time difference in milliseconds.
    :rtype: Race
    """
    races = pd.read_csv(f"{DATA_DIR}/races.csv")
    results = pd.read_csv(f"{DATA_DIR}/results.csv")
    merged_result = pd.merge(
        results.query("positionOrder == 1"),
        results.query("positionOrder == 2"),
        on="raceId",
    )[["raceId", "milliseconds_x", "milliseconds_y"]]
    merged_result = merged_result[~merged_result.isin(["\\N"]).any(axis=1)]
    merged_result["time_diff"] = merged_result["milliseconds_y"].astype(
        int
    ) - merged_result["milliseconds_x"].astype(int)
    merged_result_races = pd.merge(merged_result, races, on="raceId")[
        ["name", "year", "date", "time_diff"]
    ]
    res = merged_result_races.loc[merged_result_races["time_diff"].idxmin()]
    return Race(
        name=res["name"],
        year=int(res["year"]),
        date=res["date"],
        time_diff=res["time_diff"],
    )


print(tightestrace())
