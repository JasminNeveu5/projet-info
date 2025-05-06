import subprocess
import pandas as pd
from src.analysis.predict.codesqlern import predict_race_winner, preprocess_data, train_model
from options.config import DATA_DIR

if __name__ == "__main__":
    # main menu
    print("Do you want to rebuild the dataframe for the prediction model ?")
    print("1. Yes")
    print("2. No")
    choice = input("Enter your choice (1/2): ")
    if choice == "1":
        subprocess.run(["python3", "src/analysis/predict/pretraitement.py"])
    else:
        print("Skipping dataframe rebuild.")

    # Dummy data loading (replace with your actual data loading logic)
    # data = pd.read_csv("path/to/your/data.csv")

    # Preprocess the data
    data = pd.read_csv(f"{DATA_DIR}/df.csv")
    X, y = preprocess_data(data)

    # Train the model
    model = train_model(X, y)

    circuits_2025 = [
        "Albert Park Grand Prix Circuit",
        "Shanghai international Circuit",
        "Suzuka Circuit",
        "Bahrain International Circuit",
        "Jeddah Corniche Circuit",
        "Miami International Autodrome",
        "Autodromo Enzo e Dino Ferrari",
        "Circuit de Monaco",
        "Circuit de Barcelona-Catalunya",
        "Circuit Gilles Villeneuve",
        "Red Bull Ring",
        "Silverstone Circuit",
        "Circuit de Spa-Francorchamps",
        "Circuit Park Zandvoort",
        "Autodromo Nazionale di Monza",
        "Baku City Circuit",
        "Marina Bay Street Circuit",
        "Circuit of The Americas",
        "Autódromo Hermanos Rodríguez",
        "Autódromo José Carlos Pace",
        "Yas Marina Circuit",
    ]

    print("\nOn which circuit do you want to run the prediction for the 2025 Grand Prix?")
    for idx, circuit in enumerate(circuits_2025, 1):
        print(f"{idx}. {circuit}")
    circuit_choice = input("Enter the number of the circuit: ")
    try:
        circuit_idx = int(circuit_choice) - 1
        race = circuits_2025[circuit_idx]
    except (ValueError, IndexError):
        print("Invalid choice.")
        exit(1)

    pilotes_2025 = [
        "Lando Norris",
        "Charles Leclerc",
        "Lewis Hamilton",
        "George Russell",
        "Max Verstappen",
        "Carlos Sainz",
        "Esteban Ocon",
        "Fernando Alonso",
        "Lance Stroll",
        "Pierre Gasly",
        "Yuki Tsunoda",
        "Nico Hülkenberg",
        "Oscar Piastri"
    ]

    print(f"\nCourse: {race}\n")
    driver_probs = []
    for driver in pilotes_2025:
        will_win, probability = predict_race_winner(model, driver, race, data)
        driver_probs.append((driver, will_win, probability))

    driver_probs.sort(key=lambda x: x[2], reverse=True)

    for driver, will_win, probability in driver_probs:
        print("------\n")
        print(driver)
        print(f"{will_win}: {probability:.4f}")
