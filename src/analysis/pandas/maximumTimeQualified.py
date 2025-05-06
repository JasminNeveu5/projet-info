import pandas as pd
from options.config import DATA_DIR
from src.model.internal.race import Race  # Assuming Race is defined in model.internal.race

def get_maximumTimeQualified(race_id: int = 42):
    """
    For the race with the given race_id, return the worst (maximum) time for each qualification step (q1, q2, q3)
    as a list of Race objects.
    """

    # Load the data
    races = pd.read_csv(f"{DATA_DIR}/races.csv")
    qualifying = pd.read_csv(f"{DATA_DIR}/qualifying.csv")
    filtered_races = races.query("raceId == @race_id")
    filtered_qualifying = qualifying.query("raceId == @race_id")

    # Replace '\N' values with None (or NaN in pandas)
    races.replace(r"\\N", pd.NA, inplace=True, regex=True)
    qualifying.replace(r"\\N", pd.NA, inplace=True, regex=True)

    # Drop rows with missing values
    races.dropna(inplace=True)
    qualifying.dropna(inplace=True)

    if filtered_races.empty:
        raise ValueError(f"No race found for race_id {race_id}")

    if filtered_qualifying.empty:
        raise ValueError(f"No qualifying data found for the given race_id")

    worst_times = {
        "q1": filtered_qualifying["q1"].max(),
        "q2": filtered_qualifying["q2"].max(),
        "q3": filtered_qualifying["q3"].max(),
    }
     # Create a list of Race objects
    r = Race(
            race_id=race_id,
            year= int(filtered_races["year"].values[0]),
            name =filtered_races["name"].values[0],
            date =filtered_races["date"].values[0],
            q1_worst_time = worst_times["q1"],
            q2_worst_time = worst_times["q2"],
            q3_worst_time = worst_times["q3"],
        )

    return r
