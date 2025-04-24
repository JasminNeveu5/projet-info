from options.config import DATA_DIR
import pandas as pd
results = pd.read_csv(f"{DATA_DIR}/results.csv")
races = pd.read_csv(f"{DATA_DIR}/races.csv")
drivers = pd.read_csv(f"{DATA_DIR}/drivers.csv")
constructor_standings = pd.read_csv(f"{DATA_DIR}/constructor_standings.csv")
qualifying = pd.read_csv(f"{DATA_DIR}/qualifying.csv")
lap_times = pd.read_csv(f"{DATA_DIR}/lap_times.csv")
weather = pd.read_csv(f"{DATA_DIR}/weather.csv")

class Pretraitement:
    # renvoie le jeu de données final
    @staticmethod
    def prepare():
        df = pd.DataFrame()

        df["driver_name"] = drivers["forename"] + " " + drivers["surname"]
        df["driverId"] = drivers["driverId"]
        df = df.merge(results, on="driverId")
        df = df.merge(races, on="raceId")
        df["race_name"] = df["name"]

        # ajout des performances des courses précedentes
        df["positionN1"] = df.groupby("driverId")["positionOrder"].shift(1)
        df["positionN2"] = df.groupby("driverId")["positionOrder"].shift(2)
        df["positionN3"] = df.groupby("driverId")["positionOrder"].shift(3)

        # Vitesse moyenne sur circuit
        # Calcul de la vitesse moyenne cumulative par race_name, driver_name et year
        df.sort_values(["driver_name", "race_name", "date"], inplace=True)

        # Initialisation d'une colonne pour stocker la vitesse moyenne cumulative
        df["averageTimeCircuit"] = None

        # Boucle sur chaque combinaison de driver_name et race_name
        for (driver, race), group in df.groupby(["driver_name", "race_name"]):
            cumulative_time = []  # Liste pour stocker les vitesses cumulées
            for i, row in group.iterrows():
                # Filtrer les données jusqu'à l'année en cours (exclue)
                past_data = group[group["year"] < row["year"]]
                if not past_data.empty:
                # Calcul de la vitesse moyenne cumulative
                    past_data["milliseconds"] = past_data["milliseconds"].replace(r"\N", None)
                    past_data["milliseconds"] = pd.to_numeric(past_data["milliseconds"], errors="coerce")
                    past_data.dropna(subset=["milliseconds"], inplace=True)
                    avg_speed = past_data["milliseconds"].mean()
                else:
                    avg_speed = None  # Pas de données pour les années précédentes
                cumulative_time.append(avg_speed)

            # Ajouter les vitesses cumulées au DataFrame
            df.loc[group.index, "averageTimeCircuit"] = cumulative_time

        df = df[["driverId","driver_name","race_name","raceId","date","year","positionOrder", "grid","positionN1","positionN2","positionN3","averageTimeCircuit"]]
        df.sort_values("date", inplace=True,ascending=False)

        # Calcul de la position d'arrivée sur l'avant dernière course effectuée sur le circuit
        df["positionCircuitN1"] = df.groupby(["driverId","race_name"])["positionOrder"].shift(-1)
        df["positionCircuitN2"] = df.groupby(["driverId","race_name"])["positionOrder"].shift(-2)
        df["positionCircuitN3"] = df.groupby(["driverId","race_name"])["positionOrder"].shift(-3)

       
        # On garde uniquement les pilotes qui parcitipent à la saison 2025 et qui ont déjà conduit sur au moins une des saison précédentes.

        
        return df


data = Pretraitement.prepare()
data.dropna(inplace = True)
data.to_csv(f"{DATA_DIR}/df.csv",index = False)


