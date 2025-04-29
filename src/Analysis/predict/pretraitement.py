from options.config import DATA_DIR
import pandas as pd
import warnings
from tqdm import tqdm  # Import tqdm for progress bar

results = pd.read_csv(f"{DATA_DIR}/results.csv")
races = pd.read_csv(f"{DATA_DIR}/races.csv")
drivers = pd.read_csv(f"{DATA_DIR}/drivers.csv")
constructor_standings = pd.read_csv(f"{DATA_DIR}/constructor_standings.csv")
qualifying = pd.read_csv(f"{DATA_DIR}/qualifying.csv")
lap_times = pd.read_csv(f"{DATA_DIR}/lap_times.csv")
weather = pd.read_csv(f"{DATA_DIR}/weather.csv")
circuits = pd.read_csv(f"{DATA_DIR}/circuits.csv")
constructors = pd.read_csv(f"{DATA_DIR}/constructors.csv")


class Pretraitement:
    # renvoie le jeu de données final
    def constructorRanking(race_name, constructorRef):
        """
        Renvoie si le contructeur a gagné sur le circuit
        `race_name` en n-1, n-2 ou n-3.

        :return: Un tuple contenant trois valeurs booléennes :
            - n1 : True si le constructeur a gagné en n-1
            - n2 : True si le constructeur a gagné en n-2
            - n3 : True si le constructeur a gagné en n-3
        """
        # création de la table de travail
        table_travail = pd.DataFrame()

        table_travail["constructorRef"] = constructors["constructorRef"]
        table_travail["constructorId"] = constructors["constructorId"]
        table_travail = table_travail.merge(constructor_standings, on="constructorId")
        table_travail = table_travail.merge(races, on="raceId")
        table_travail = table_travail.merge(circuits, on="circuitId")
        table_travail["race_name"] = table_travail["name_y"]

        # filtrer pour ne récuperer que les constucteurs de l'année sur le circuit

        table_travail = table_travail[table_travail["constructorRef"] == constructorRef]
        table_travail = table_travail[table_travail["race_name"] == race_name]
        table_travail = table_travail[["constructorRef", "race_name", "wins", "year"]]

        # récupere les 3 plus récentes années
        recent_years = table_travail["year"].dropna().unique()
        recent_years = sorted(recent_years, reverse=True)[
            :3
        ]  # Get the three most recent years

        n1 = (
            table_travail[table_travail["year"] == recent_years[0]]["wins"].iloc[0]
            if len(recent_years) > 0
            and not table_travail[table_travail["year"] == recent_years[0]].empty
            else 0
        )
        n2 = (
            table_travail[table_travail["year"] == recent_years[1]]["wins"].iloc[0]
            if len(recent_years) > 1
            and not table_travail[table_travail["year"] == recent_years[1]].empty
            else 0
        )
        n3 = (
            table_travail[table_travail["year"] == recent_years[2]]["wins"].iloc[0]
            if len(recent_years) > 2
            and not table_travail[table_travail["year"] == recent_years[2]].empty
            else 0
        )

        return (int(n1), int(n2), int(n3))

    @staticmethod
    def prepare():
        df = pd.DataFrame()

        df["driver_name"] = drivers["forename"] + " " + drivers["surname"]
        df["driverId"] = drivers["driverId"]
        df = df.merge(results, on="driverId")
        df = df.merge(races, on="raceId")
        df = df.merge(circuits, on="circuitId")
        df = df.merge(constructors, on="constructorId")
        df["race_name"] = df["name_y"]

        # Keeping values only coherent with the 2025 season
        # (https://fr.wikipedia.org/wiki/Championnat_du_monde_de_Formule_1_2025#Grands_Prix_de_la_saison_2025)

        # List of circuits for the 2025 season
        circuits_2025 = [
            "Albert Park Grand Prix Circuit",
            "Shanghai international Circuit",
            "Suzuka Circuit",
            "Bahrain International Circuit",
            "Jeddah Corniche Circuit",
            "Miami International Autodrome",  # never trained
            "Autodromo Enzo e Dino Ferrari",
            "Circuit de Monaco",
            "Circuit de Barcelona-Catalunya",
            "Circuit Gilles Villeneuve",
            "Red Bull Ring",
            "Silverstone Circuit",
            "Circuit de Spa-Francorchamps",
            "Circuit Magyar Nagydij",  # not in circuits.csv
            "Circuit Park Zandvoort",
            "Autodromo Nazionale di Monza",
            "Baku City Circuit",
            "Marina Bay Street Circuit",
            "Circuit of The Americas",
            "Autódromo Hermanos Rodríguez",
            "Autódromo José Carlos Pace",
            "Circuit Silver Las Vegas",  # not in circuits.csv
            "Lusail international Circuit",  # not in circuits.csv
            "Yas Marina Circuit",
        ]

        # Filter the DataFrame to keep only rows with circuits in the 2025 season
        df = df[df["race_name"].isin(circuits_2025)]

        # On garde uniquement les pilotes qui parcitipent à la saison 2025
        # et qui ont déjà conduit sur au moins une des saison précédentes.

        pilotes_2025 = [
            "Lando Norris",
            "Oscar Piastri",
            "Charles Leclerc",
            "Lewis Hamilton",
            "George Russell",
            "Max Verstappen",
            "Liam Lawson",
            "Alexander Albon",
            "Carlos Sainz",
            "Esteban Ocon",
            "Oliver Bearman",
            "Fernando Alonso",
            "Lance Stroll",
            "Pierre Gasly",
            "Yuki Tsunoda",
            "Nico Hülkenberg",
        ]

        df = df[df["driver_name"].isin(pilotes_2025)]

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
        grouped = df.groupby(["driver_name", "race_name"])
        for (driver, race), group in tqdm(grouped, desc="Processing drivers and races"):
            cumulative_time = []  # Liste pour stocker les vitesses cumulées
            for i, row in group.iterrows():
                # Filtrer les données jusqu'à l'année en cours (exclue)
                past_data = group[group["year"] < row["year"]]
                if not past_data.empty:
                    # Calcul de la vitesse moyenne cumulative
                    past_data["milliseconds"] = past_data["milliseconds"].replace(
                        r"\N", None
                    )
                    past_data["milliseconds"] = pd.to_numeric(
                        past_data["milliseconds"], errors="coerce"
                    )
                    past_data.dropna(subset=["milliseconds"], inplace=True)
                    avg_speed = past_data["milliseconds"].mean()
                else:
                    avg_speed = None  # Pas de données pour les années précédentes
                cumulative_time.append(avg_speed)

            # Ajouter les vitesses cumulées au DataFrame
            df.loc[group.index, "averageTimeCircuit"] = cumulative_time

        df = df[
            [
                "driverId",
                "constructorRef",
                "driver_name",
                "race_name",
                "raceId",
                "date",
                "year",
                "positionOrder",
                "grid",
                "positionN1",
                "positionN2",
                "positionN3",
                "averageTimeCircuit",
            ]
        ]
        df.sort_values("date", inplace=True, ascending=False)

        # Calcul de la position d'arrivée sur l'avant
        # dernière course effectuée sur le circuit
        df["positionCircuitN1"] = df.groupby(["driverId", "race_name"])[
            "positionOrder"
        ].shift(-1)
        df["positionCircuitN2"] = df.groupby(["driverId", "race_name"])[
            "positionOrder"
        ].shift(-2)
        df["positionCircuitN3"] = df.groupby(["driverId", "race_name"])[
            "positionOrder"
        ].shift(-3)

        # Calcul du numéro de qualification sur les
        # dernières courses effectuées sur le circuit
        df["qualifCircuitN1"] = df.groupby(["driverId", "race_name"])["grid"].shift(-1)
        df["qualifCircuitN2"] = df.groupby(["driverId", "race_name"])["grid"].shift(-2)
        df["qualifCircuitN3"] = df.groupby(["driverId", "race_name"])["grid"].shift(-3)

        # Replace grid positions with qualification groups
        def grid_to_qualif_group(grid_position):
            if 1 <= grid_position <= 10:
                return "3"
            elif 11 <= grid_position <= 15:
                return "2"
            # elif 16 <= grid_position:
            #     return "q1"
            else:
                return "1"

        df["qualifCircuitN1"] = df["qualifCircuitN1"].apply(
            lambda x: grid_to_qualif_group(x) if pd.notna(x) else "1"
        )
        df["qualifCircuitN2"] = df["qualifCircuitN2"].apply(
            lambda x: grid_to_qualif_group(x) if pd.notna(x) else "1"
        )
        df["qualifCircuitN3"] = df["qualifCircuitN3"].apply(
            lambda x: grid_to_qualif_group(x) if pd.notna(x) else "1"
        )

        # Nombre de victoires constructeurs

        # Add constructorN1, constuctorN2, constructorN3 columns using constructorRanking method
        tqdm.pandas(desc="Processing constructor rankings (1/3)")
        df["constructorN1"] = df.progress_apply(
            lambda row: (
                Pretraitement.constructorRanking(
                    row["race_name"], row["constructorRef"]
                )[0]
                if pd.notna(row["race_name"]) and pd.notna(row["constructorRef"])
                else 0
            ),
            axis=1,
        )
        tqdm.pandas(desc="Processing constructor rankings (2/3)")
        df["constructorN2"] = df.progress_apply(
            lambda row: (
                Pretraitement.constructorRanking(
                    row["race_name"], row["constructorRef"]
                )[1]
                if pd.notna(row["race_name"]) and pd.notna(row["constructorRef"])
                else 0
            ),
            axis=1,
        )
        tqdm.pandas(desc="Processing constructor rankings (3/3)")
        df["constructorN3"] = df.progress_apply(
            lambda row: (
                Pretraitement.constructorRanking(
                    row["race_name"], row["constructorRef"]
                )[2]
                if pd.notna(row["race_name"]) and pd.notna(row["constructorRef"])
                else 0
            ),
            axis=1,
        )

        return df


with warnings.catch_warnings():
    warnings.simplefilter(
        "ignore"
    )  # Suppress warnings : boring stuff from pandas (clueless)
    data = Pretraitement.prepare()

    # Fill NaN values with the mean for each driver and each circuit
    numeric_columns = data.select_dtypes(include=["number"]).columns
    for column in numeric_columns:
        data[column] = data.groupby(["driver_name", "race_name"])[column].transform(
            lambda x: x.fillna(x.mean())
        )

    # Fill remaining NaNs for numeric columns with the overall mean
    data[numeric_columns] = data[numeric_columns].fillna(data[numeric_columns].mean())

    # Fill remaining NaNs for object (categorical) columns with mode or a placeholder
    object_columns = data.select_dtypes(include=["object"]).columns
    for column in object_columns:
        mode = data[column].mode()
        if not mode.empty:
            data[column] = data[column].fillna(mode[0])
        else:
            data[column] = data[column].fillna("unknown")

    # Fill any remaining NaNs with 0 as a last resort
    data = data.fillna(0)

    data.to_csv(f"{DATA_DIR}/df.csv", index=False)
