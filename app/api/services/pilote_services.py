import pandas as pd
from options.config import DATA_DIR


class DefaultQuery:

    @staticmethod
    def nombre_victoire(nb_victoires):
        results = pd.read_csv(f"{DATA_DIR}/results.csv")
        drivers = pd.read_csv(f"{DATA_DIR}/drivers.csv")
        return (
            pd.merge(results, drivers, on="driverId")
            .query("position == '1'")
            .groupby(["driverId", "forename", "surname"])
            .size()
            .reset_index(name="Victoires")
            .query(f"Victoires >= {nb_victoires}")
            .sort_values("Victoires", ascending=False)
            .to_json(orient="records")
        )

    @staticmethod
    def classement(annee):

        results = pd.read_csv(f"{DATA_DIR}/results.csv")
        drivers = pd.read_csv(f"{DATA_DIR}drivers.csv")
        races = pd.read_csv(f"{DATA_DIR}/races.csv")

        races_year = pd.merge(results, races[races["year"] == annee],
                              on="raceId")
        races_year["positionOrder"] = races_year["positionOrder"].astype(int)
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
        return pd.merge(sorted_drivers, drivers, on="driverId")[
            ["forename", "surname", "points"]
        ].to_json(orient="records")

    @staticmethod
    def meilleur_temps(location: str):
        drivers = pd.read_csv(f"{DATA_DIR}drivers.csv")
        races = pd.read_csv(f"{DATA_DIR}/races.csv")
        circuits = pd.read_csv(f"{DATA_DIR}circuits.csv")
        lap_times = pd.read_csv(f"{DATA_DIR}/lap_times.csv")

        def conversion(milliseconds):
            minutes = milliseconds // 60000
            seconds = (milliseconds % 60000) // 1000
            millis = milliseconds % 1000
            return f"{minutes}m {seconds}s {millis}ms"

        merged_data = pd.merge(lap_times, races, on="raceId")
        merged_data = pd.merge(merged_data, circuits, on="circuitId")
        best_laps_per_race = merged_data.loc[
            merged_data.groupby("raceId")["milliseconds"].idxmin()
        ]
        best_laps_per_race = pd.merge(best_laps_per_race, drivers,
                                      on="driverId")
        best_laps_per_circuit = best_laps_per_race.loc[
            best_laps_per_race.groupby("circuitId")["milliseconds"].idxmin()
        ]
        best_laps_per_circuit["meilleur_temps_ever"] = best_laps_per_circuit[
            "milliseconds"
        ].apply(conversion)
        result = best_laps_per_circuit[
            ["location", "meilleur_temps_ever", "forename", "surname", "year"]
        ]
        result = result.rename(
            columns={
                "location": "Circuit",
                "meilleur_temps_ever": "Best_Lap_Time",
                "forename": "Driver_First_Name",
                "surname": "Driver_Last_Name",
                "year": "Year",
                "name": "Race_Name",
            }
        )
        return (result.query(f"Circuit == '{location}'")
                      .to_json(orient="records"))
