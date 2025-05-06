import subprocess
import pandas as pd
import time
from .src.analysis.predict.codesqlern import predict_race_winner, preprocess_data, train_model
from .options.config import DATA_DIR

circuits_2025 = [
    "Albert Park Grand Prix Circuit",
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

def print_intro():
    print("Project Data Processing Group 12 (2024/2025) is proud to present")
    time.sleep(1)
    for _ in range(len("Project Data Processing Group 12 (2024/2025) is proud to present")):
        print(".", end="", flush=True)
        time.sleep(0.02)
    print('\n')
    print(r"""                ____                         _ ____  _     
               / ___|_ __ ___  _   _ _ __   / |___ \( )___ 
              | |  _| '__/ _ \| | | | '_ \  | | __) |// __|
              | |_| | | | (_) | |_| | |_) | | |/ __/  \__ \
               \____|_|  \___/ \__,_| .__/  |_|_____| |___/
                                    |_|                    
                                _                     
                _ __ ___   __ _(_)_ __    _ __  _   _ 
               | '_ ` _ \ / _` | | '_ \  | '_ \| | | |
               | | | | | | (_| | | | | |_| |_) | |_| |
               |_| |_| |_|\__,_|_|_| |_(_) .__/ \__, |
                                         |_|    |___/ 
          """)
    time.sleep(.5)
    print("\n")

def rebuild_dataframe():
    print("Rebuilding dataframe for the prediction model...")
    subprocess.run(["python3", "projet-info/src/analysis/predict/pretraitement.py"])
    print("Dataframe rebuilt.\n")

def load_and_train():
    try:
        data = pd.read_csv(f"{DATA_DIR}/df.csv")
        X, y = preprocess_data(data)
        model = train_model(X, y)
        return model, data
    except Exception as e:
        print(f"Error loading or training model: {e}")
        return None, None

def predict_menu(model, data):
    print("\nOn which circuit do you want to run the prediction for the 2025 Grand Prix?")
    for idx, circuit in enumerate(circuits_2025, 1):
        print(f"{idx}. {circuit}")
    circuit_choice = input("Enter the number of the circuit: ")
    try:
        circuit_idx = int(circuit_choice) - 1
        race = circuits_2025[circuit_idx]
    except (ValueError, IndexError):
        print("Invalid choice.")
        return

    print(f"\nCourse: {race}\n")
    driver_probs = []
    for driver in pilotes_2025:
        try:
            will_win, probability = predict_race_winner(model, driver, race, data)
            driver_probs.append((driver, will_win, probability))
        except Exception as e:
            print(f"Prediction error for {driver}: {e}")
            driver_probs.append((driver, "Error", 0.0))

    driver_probs.sort(key=lambda x: x[2], reverse=True)

    for driver, will_win, probability in driver_probs:
        print("------\n")
        print(driver)
        print(f"{will_win}: {probability:.4f}")

def launch_question():
    """
    Function to run analysis questions from the pandas folder.
    Allows users to select which analysis to run and input required parameters.
    """
    import importlib
    import inspect
    import os

    # Get all python files from the pandas folder (excluding __init__.py and __pycache__)
    pandas_dir = os.path.join("projet-info","src", "analysis", "pandas")
    analysis_files = [f[:-3] for f in os.listdir(pandas_dir)
                     if f.endswith('.py') and f != '__init__.py' and not f.startswith('test')]

    # Display the menu
    print("\nAvailable analyses:")
    for idx, analysis in enumerate(analysis_files, 1):
        print(f"{idx}. {analysis}")

    # Get user choice
    try:
        choice = int(input("Enter the number of the analysis to run: "))
        if choice < 1 or choice > len(analysis_files):
            print("Invalid choice.")
            return
    except ValueError:
        print("Please enter a number.")
        return

    selected_analysis = analysis_files[choice - 1]

    try:
        # Import the selected analysis module
        module_name = f"src.analysis.pandas.{selected_analysis}"
        module = importlib.import_module(module_name)

        # Try to find the main function (usually named the same as the file)
        main_function = None
        for name, obj in inspect.getmembers(module):
            if inspect.isfunction(obj) and name == selected_analysis:
                main_function = obj
                break

        if main_function is None:
            # If no function with same name exists, look for any function
            for name, obj in inspect.getmembers(module):
                if inspect.isfunction(obj) and not name.startswith('_'):
                    main_function = obj
                    break

        if main_function:
            # Get function parameters
            params = inspect.signature(main_function).parameters
            args = []

            # Ask for each parameter
            for param_name, param in params.items():
                # Try to determine parameter type from annotations or default value
                param_type = param.annotation if param.annotation != inspect.Parameter.empty else "string"
                type_hint = f" ({param_type.__name__})" if hasattr(param_type, "__name__") else ""

                # Show default value if available
                default_hint = ""
                if param.default != inspect.Parameter.empty:
                    default_hint = f" [default: {param.default}]"

                # Prompt for input
                value = input(f"Enter {param_name}{type_hint}{default_hint}: ")

                # Use default if input is empty and default exists
                if value == "" and param.default != inspect.Parameter.empty:
                    args.append(param.default)
                else:
                    # Convert to proper type if possible
                    if param_type == int:
                        args.append(int(value))
                    elif param_type == float:
                        args.append(float(value))
                    elif param_type == bool:
                        args.append(value.lower() in ('yes', 'true', 't', 'y', '1'))
                    else:
                        args.append(value)

            # Call the function with gathered parameters
            print('\n')
            print(f"\nRunning {selected_analysis}...\n")
            result = main_function(*args)

            # Display the result
            if result is not None:
                if isinstance(result, list):
                    for item in result:
                        print(item)
                else:
                    print(result)
                    print('\n')
        else:
            print(f"No callable function found in {selected_analysis}. The file might run on import.")

    except Exception as e:
        print(f"Error running the analysis: {str(e)}")

def main_menu():
    print_intro()
    # model, data = None, None
    while True:
        print("Main Menu:")
        print("1. Rebuild dataframe for the prediction model")
        print("2. Run prediction for a 2025 Grand Prix circuit")
        print("3. Run analysis questions")  # New option
        print("4. Exit")
        choice = input("Enter your choice (1/2/3/4): ")
        if choice == "1":
            rebuild_dataframe()
            model, data = load_and_train()
        elif choice == "2":
            predict_menu(model, data)
        elif choice == "3":
            launch_question()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.\n")

if __name__ == "__main__":
    main_menu()
