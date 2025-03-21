from fastapi import HTTPException
import pandas as pd


class Question:

    @staticmethod
    def q1(nb_victoires: int):
        if nb_victoires < 0:
            raise HTTPException(status_code=404,
                                detail="Nombre de victoires invalide")
        results = pd.read_csv("../../data/results.csv")
        drivers = pd.read_csv("../../data/drivers.csv")
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
    def q2(self, annee: int):
        if annee < 1950 or annee > 2024:
            raise HTTPException(status_code=404, detail="Année invalide")
        results = pd.read_csv("../../data/results.csv")
        drivers = pd.read_csv("../..//data/drivers.csv")
        races = pd.read_csv("../../data/races.csv")
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
