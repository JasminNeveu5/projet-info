from src.Common.utils import merge_dicts, read_csv, time_to_seconds
from options.config import DATA_DIR

# Lire les données
qualif = read_csv(f"{DATA_DIR}/qualifying.csv")
circuits = read_csv(f"{DATA_DIR}/circuits.csv")
races = read_csv(f"{DATA_DIR}/races.csv")

# Fusionner les courses et les circuits par circuitId
races_plus_circuits = merge_dicts(races, circuits, "circuitId")

# Préparer les données intéressantes avec les temps de qualification et les références des circuits
interesting_datas = []
for row in qualif:
    race_id = row["raceId"]
    # Find the corresponding race data (merged with circuits)
    race_data = next(
        (race for race in races_plus_circuits if race["raceId"] == race_id), None
    )
    if race_data:
        interesting_datas.append(
            {
                "circuitId": race_data["circuitId"],
                "circuitRef": race_data["circuitRef"],
                "q1": row["q1"].strip('"').strip() if row["q1"] != "\\N" else None,
                "q2": row["q2"].strip('"').strip() if row["q2"] != "\\N" else None,
                "q3": row["q3"].strip('"').strip() if row["q3"] != "\\N" else None,
            }
        )

# Remplacer '\N' par None et convertir en secondes
for data in interesting_datas:
    data["q1"] = time_to_seconds(data["q1"]) if data["q1"] else None
    data["q2"] = time_to_seconds(data["q2"]) if data["q2"] else None
    data["q3"] = time_to_seconds(data["q3"]) if data["q3"] else None

# Préparer les colonnes pour les temps
q1_column = sorted([data["q1"] for data in interesting_datas if data["q1"] is not None])
q1_column.pop()  # REMOVED the weird value created by merge
q2_column = [data["q2"] for data in interesting_datas if data["q2"] is not None]
q3_column = [data["q3"] for data in interesting_datas if data["q3"] is not None]

# Trouver les temps maximum de qualification
max_q1 = max(q1_column) if q1_column else None
max_q2 = max(q2_column) if q2_column else None
max_q3 = max(q3_column) if q3_column else None

# Affichage des résultats
print(f"Max Q1: {max_q1}, Max Q2: {max_q2}, Max Q3: {max_q3}")


# Regrouper par circuitId pour trouver les temps maximum de qualification par circuit
circuit_times = {}
for data in interesting_datas:
    circuit_id = data["circuitId"]
    if circuit_id.lower() not in map(str.lower, circuit_times.keys()):
        circuit_times[circuit_id] = {"q1": [], "q2": [], "q3": []}

    # Append times to the appropriate circuit
    if data["q1"] is not None:
        circuit_times[circuit_id]["q1"].append(data["q1"])
    if data["q2"] is not None:
        circuit_times[circuit_id]["q2"].append(data["q2"])
    if data["q3"] is not None:
        circuit_times[circuit_id]["q3"].append(data["q3"])

# Calculer le temps maximum par circuit
for circuit_id, times in circuit_times.items():
    max_q1_circuit = max(times["q1"]) if times["q1"] else None
    max_q2_circuit = max(times["q2"]) if times["q2"] else None
    max_q3_circuit = max(times["q3"]) if times["q3"] else None
    # Affichage des résultats par circuit_id
    print(
        f"Circuit {circuit_id}: Max Q1: {max_q1_circuit}, Max Q2: {max_q2_circuit}, Max Q3: {max_q3_circuit}"
    )
