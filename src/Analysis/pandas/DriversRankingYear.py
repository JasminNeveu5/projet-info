import pandas as pd
from options.config import DATA_DIR
from src.Model.Driver import Driver

# Points tables
GP_POINTS = {1: 25, 2: 18, 3: 15, 4: 12, 5: 10, 6: 8, 7: 6, 8: 4, 9: 2, 10: 1}
SPRINT_POINTS = {1: 8, 2: 7, 3: 6, 4: 5, 5: 4, 6: 3, 7: 2, 8: 1}
FASTEST_LAP_POINTS = 1  # Points for the fastest lap

def get_points(row):
    pos = row["positionOrder"]
    if row["Sprint"]:
        return SPRINT_POINTS.get(pos, 0)
    else:
        return GP_POINTS.get(pos, 0)

def get_ranking_year(year: int):
    if not isinstance(year, int):
        raise TypeError("year doit être de type int")
    if year < 1950 or year > 2024:
        raise ValueError("year doit être compris entre 1950 et 2024")
    results = pd.read_csv(f"{DATA_DIR}/results.csv")
    drivers = pd.read_csv(f"{DATA_DIR}/drivers.csv")
    races = pd.read_csv(f"{DATA_DIR}/races.csv")

    # Ensure 'Sprint' column exists in races DataFrame
    if "Sprint" not in races.columns:
        races["Sprint"] = False  # Default to False if not present

    races_year = pd.merge(results, races[races["year"] == year][["raceId", "Sprint"]], on="raceId")
    races_year["positionOrder"] = races_year["positionOrder"].astype(int)
    races_year["points"] = races_year.apply(get_points, axis=1)

    # Add points for fastest lap
    fastest_lap = races_year[(races_year["fastestLap"] != 0)]
    races_year.loc[fastest_lap.index, "points"] += FASTEST_LAP_POINTS

    points_wins = (
        races_year.groupby("driverId")
        .agg(
            points=("points", "sum"),
            wins=("positionOrder", lambda x: (x == 1).sum()),
            second_places=("positionOrder", lambda x: (x == 2).sum()),
            third_places=("positionOrder", lambda x: (x == 3).sum()),
        )
        .reset_index()
    )

    sorted_drivers = points_wins.sort_values(
        by=["points", "wins", "second_places", "third_places"],
        ascending=[False, False, False, False],
    )

    r = pd.merge(sorted_drivers, drivers, on="driverId")[
        ["driverId", "forename", "surname", "nationality", "points"]
    ]

    result = []
    for index, row in r.iterrows():
        result.append(
            Driver(
                forename=row["forename"],
                surname=row["surname"],
                nationality=row["nationality"],
                nb_points=row["points"],
            )
        )
    return result

if __name__ == "__main__":
    year = 2023
    ranking = get_ranking_year(year)
    for driver in ranking:
        print(
            f"{driver.forename} {driver.surname} ({driver.nationality}) - Points: {driver.additional_info['nb_points']}")
