import pandas as pd
from options.config import DATA_DIR
from src.model.internal.driver import Driver
from src.common.utils import time_to_seconds


def get_driver_ranking(
    year: int, results_csv_path: str, sprint_results_csv_path: str
) -> list:
    # Load data
    df_gp = pd.read_csv(results_csv_path)
    df_sprint = pd.read_csv(sprint_results_csv_path)
    races = pd.read_csv(f"{DATA_DIR}/races.csv")
    drivers = pd.read_csv(f"{DATA_DIR}/drivers.csv")

    # Filter races by year
    races_year = races[races["year"] == year][["raceId"]]
    race_ids = set(races_year["raceId"])
    df_gp = df_gp[df_gp["raceId"].isin(race_ids)]
    df_sprint = df_sprint[df_sprint["raceId"].isin(race_ids)]

    # --- Grand Prix points (use 'points' column directly) ---
    df_gp["gp_points"] = df_gp["points"].fillna(0)

    # --- Fastest lap (MT) bonus ---
    df_gp["fastestLapTime_sec"] = df_gp["fastestLapTime"].apply(time_to_seconds)
    df_gp["mt_point"] = 0

    for race_id, group in df_gp.groupby("raceId"):
        classified = group[
            (group["positionOrder"] <= 10) & (group["fastestLapTime_sec"].notnull())
        ]
        if not classified.empty:
            min_time = classified["fastestLapTime_sec"].min()
            fastest_driver = classified[
                classified["fastestLapTime_sec"] == min_time
            ].iloc[0]
            idx = fastest_driver.name
            df_gp.at[idx, "mt_point"] = 1

    # --- Sprint points (use 'points' column directly) ---
    df_sprint["sprint_points"] = df_sprint["points"].fillna(0)

    # --- Aggregate all points ---
    gp_points_sum = df_gp.groupby("driverId")["gp_points"].sum()
    mt_points_sum = df_gp.groupby("driverId")["mt_point"].sum()
    sprint_points_sum = df_sprint.groupby("driverId")["sprint_points"].sum()

    # Do NOT add mt_points to total_points
    total_points = gp_points_sum.add(sprint_points_sum, fill_value=0)

    # Merge with driver info and points breakdown
    ranking = total_points.reset_index(name="total_points").sort_values(
        "total_points", ascending=False
    )
    ranking = ranking.merge(drivers, on="driverId", how="left")
    ranking = ranking.merge(
        gp_points_sum.reset_index(name="grand_prix_points"), on="driverId", how="left"
    )
    ranking = ranking.merge(
        sprint_points_sum.reset_index(name="sprint_points"), on="driverId", how="left"
    )
    ranking = ranking.merge(
        mt_points_sum.reset_index(name="mt_points"), on="driverId", how="left"
    )

    # Build Driver objects list
    driver_list = []
    for _, row in ranking.iterrows():
        driver = Driver(
            forename=row.get("forename", ""),
            surname=row.get("surname", ""),
            nationality=row.get("nationality", ""),
            total_points=row["total_points"],
            grand_prix_points=row["grand_prix_points"],
            sprint_points=row["sprint_points"],
            mt_points=row["mt_points"],
        )
        driver_list.append(driver)

    return driver_list

if __name__ == "__main__":
    # Example usage:
    ranking_2021 = get_driver_ranking(
        2021, f"{DATA_DIR}/results.csv", f"{DATA_DIR}/sprint_results.csv"
    )
    for driver in ranking_2021:
        print(driver)
