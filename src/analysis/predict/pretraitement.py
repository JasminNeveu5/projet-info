import pandas as pd
import warnings
from tqdm import tqdm  # Import tqdm for progress bar
from options.config import DATA_DIR

results = pd.read_csv(f"{DATA_DIR}/results.csv")
races = pd.read_csv(f"{DATA_DIR}/races.csv")
drivers = pd.read_csv(f"{DATA_DIR}/drivers.csv")
constructor_standings = pd.read_csv(f"{DATA_DIR}/constructor_standings.csv")
qualifying = pd.read_csv(f"{DATA_DIR}/qualifying.csv")
lap_times = pd.read_csv(f"{DATA_DIR}/lap_times.csv")
weather = pd.read_csv(f"{DATA_DIR}/weather.csv")
circuits = pd.read_csv(f"{DATA_DIR}/circuits.csv")


class Pretraitement:
    # renvoie le jeu de données final
    @staticmethod
    def prepare():
        df = pd.DataFrame()

        df["driver_name"] = drivers["forename"] + " " + drivers["surname"]
        df["driverId"] = drivers["driverId"]
        df = df.merge(results, on="driverId")
        df = df.merge(races, on="raceId")
        df = df.merge(circuits, on="circuitId")
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

        # Replace grid positions with qualification groups as integers
        def grid_to_qualif_group(grid_position):
            if 1 <= grid_position <= 10:
                return 3  # q3
            elif 11 <= grid_position <= 15:
                return 2  # q2
            else:
                return 1  # q1

        df["qualifCircuitN1"] = df["qualifCircuitN1"].apply(
            lambda x: grid_to_qualif_group(x) if pd.notna(x) else 1
        )
        df["qualifCircuitN2"] = df["qualifCircuitN2"].apply(
            lambda x: grid_to_qualif_group(x) if pd.notna(x) else 1
        )
        df["qualifCircuitN3"] = df["qualifCircuitN3"].apply(
            lambda x: grid_to_qualif_group(x) if pd.notna(x) else 1
        )

    # Fill NA values for each driver and each circuit with their respective means, else 0 if not enough data

        # Group 1: positionN1, positionN2, positionN3
        pos_cols = ["positionN1", "positionN2", "positionN3"]

        # Compute row-wise mean for the three columns, ignoring NA
        pos_row_means = df[pos_cols].mean(axis=1, skipna=True)

        # Fill NA values in each column with the row-wise mean
        for col in pos_cols:
            df[col] = df[col].fillna(pos_row_means)

        # If still NA (all three were NA), fill with 0
        for col in pos_cols:
            df[col] = df[col].fillna(0)

        # Group 2: averageTimeCircuit
        df["averageTimeCircuit"] = df.groupby(["driverId", "race_name"])["averageTimeCircuit"].transform(
            lambda x: x.fillna(x.mean())
        )
        df["averageTimeCircuit"] = df.groupby("driverId")["averageTimeCircuit"].transform(
            lambda x: x.fillna(x.mean())
        )
        df["averageTimeCircuit"] = df["averageTimeCircuit"].fillna(0)

        # Group 3: positionCircuitN1, positionCircuitN2, positionCircuitN3
        circuit_cols = ["positionCircuitN1", "positionCircuitN2", "positionCircuitN3"]

        # Compute row-wise mean for the three columns, ignoring NA
        row_means = df[circuit_cols].mean(axis=1, skipna=True)

        # Fill NA values in each column with the row-wise mean
        for col in circuit_cols:
            df[col] = df[col].fillna(row_means)

        # If still NA (all three were NA), fill with 0
        for col in circuit_cols:
            df[col] = df[col].fillna(0)

        print(df["driver_name"].unique())
        return df


# Adding a progress bar for the preparation process

with warnings.catch_warnings():
    warnings.simplefilter(
        "ignore"
    )  # Suppress warnings : boring stuff from pandas (clueless)
    data = Pretraitement.prepare()
    # data.dropna(inplace=True)
    data.to_csv(f"{DATA_DIR}/df.csv", index=False)

# Adding constructor-related data
import pandas as pd
from tqdm import tqdm  # For progress bars

# Load the necessary dataframes
df = pd.read_csv(f"{DATA_DIR}/df.csv")
constructors_df = pd.read_csv(f"{DATA_DIR}/constructors.csv")
constructor_results_df = pd.read_csv(f"{DATA_DIR}/constructor_results.csv")
results_df = pd.read_csv(f"{DATA_DIR}/results.csv")  # Need this to link drivers to constructors

# Step 1: Get constructorId for each driver-race combination
print("Merging driver data with constructor information...")
# First, ensure df has constructorId by merging with results
if 'constructorId' not in df.columns:
    df = df.merge(results_df[['raceId', 'driverId', 'constructorId']], on=['raceId', 'driverId'])

# Step 2: Merge with constructors to get constructorRef
df = df.merge(constructors_df[['constructorId', 'constructorRef']], on='constructorId')

# Step 3: Calculate historical constructor points for each circuit
print("Calculating historical constructor results by circuit...")
# Create a dataframe with constructor points for each race at each circuit
constructor_points = constructor_results_df.merge(constructors_df[['constructorId', 'constructorRef']], 
                                                on='constructorId')

# Now get race information (including circuit)
races_df = pd.read_csv(f"{DATA_DIR}/races.csv")
constructor_points = constructor_points.merge(races_df[['raceId', 'name', 'date', 'year']], on='raceId')

# Sort by date to get correct historical order
constructor_points = constructor_points.sort_values(['name', 'constructorRef', 'date'])

# Calculate the historical points (N1, N2, N3) for each constructor at each circuit
constructor_points['constructorResultsN1'] = constructor_points.groupby(['name', 'constructorRef'])['points'].shift(1)
constructor_points['constructorResultsN2'] = constructor_points.groupby(['name', 'constructorRef'])['points'].shift(2)
constructor_points['constructorResultsN3'] = constructor_points.groupby(['name', 'constructorRef'])['points'].shift(3)

# Step 4: Merge the historical points back to the main dataframe
print("Adding constructor history columns to dataframe...")
# We need to join based on raceId and constructorId
df = df.merge(
    constructor_points[['raceId', 'constructorId', 'constructorResultsN1', 'constructorResultsN2', 'constructorResultsN3']],
    on=['raceId', 'constructorId'],
    how='left'  # Use left join to keep all df rows
)

# Step 5: Fill NaN values with 0 for races where there's no prior data
df[['constructorResultsN1', 'constructorResultsN2', 'constructorResultsN3']] = \
    df[['constructorResultsN1', 'constructorResultsN2', 'constructorResultsN3']].fillna(0)

df.to_csv(f"{DATA_DIR}/df.csv", index=False)
