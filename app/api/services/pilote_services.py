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


    @staticmethod
    def temps_min_qualif_annee(circuit: str, annee: str):
        qualif = pd.read_csv(f"{DATA_DIR}/qualifying.csv")
        circuits = pd.read_csv(f"{DATA_DIR}/circuits.csv")
        races = pd.read_csv(f"{DATA_DIR}/races.csv")

        # On construit la table avec que les données importantes + selection de l'année
        races = races.query(f"year == {annee}")
        races_plus_circuits = pd.merge(races, circuits, on="circuitId")

        interesting_datas = pd.merge(qualif, races_plus_circuits, on="raceId")[
            ["circuitId", "circuitRef", "q1", "q2", "q3","name_x"]]

        # On remplace les "\N" (non-qualifiés) par None pour pouvoir les enlever facilement
        interesting_datas['q1'] = interesting_datas['q1'].replace(r'\N', None)
        interesting_datas['q2'] = interesting_datas['q2'].replace(r'\N', None)
        interesting_datas['q3'] = interesting_datas['q3'].replace(r'\N', None)

        # Group by circuitId
        interesting_datas_by_circuit = interesting_datas.groupby("circuitRef")

        # Create a dictionary of times per circuitId and qualifier
        times_by_circuit_and_qual = {}
        for circuitRef, group in interesting_datas_by_circuit:
            for qual in ['q1', 'q2', 'q3']:
                times = group[qual].dropna().tolist()
                times_by_circuit_and_qual[(circuitRef, qual)] = times

        # Compute the maximum time for each (circuitId, qualifier)
        max_times_by_circuit_and_qual = {key: max(times) for key, times in times_by_circuit_and_qual.items() if times}

        requete = circuit
        max_time = {q: max_times_by_circuit_and_qual.get((requete, q), None) for q in ['q1', 'q2', 'q3']}

        return max_time