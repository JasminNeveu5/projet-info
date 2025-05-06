import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report
from sklearn.pipeline import make_pipeline
from options.config import DATA_DIR

# Load your dataset (replace with your actual data source)
# Assuming you have a CSV file with the structure you described
data = pd.read_csv(f"{DATA_DIR}/df.csv")


# Preprocess the data
def preprocess_data(df):
    # Create the target variable - whether the driver won the race (positionOrder == 1)
    df["won_race"] = df["positionOrder"] == 1

    # Convert categorical variables to numerical (if needed)
    df = pd.get_dummies(df, columns=["driver_name", "race_name"], drop_first=False)

    # Select features - adjust based on your feature importance analysis
    features = [
        "grid",
        "positionN1",
        "positionN2",
        "positionN3",
        "averageTimeCircuit",
        "positionCircuitN1",
        "positionCircuitN2",
        "positionCircuitN3",
    ]

    # Add the one-hot encoded columns for drivers and races
    driver_cols = [col for col in df.columns if col.startswith("driver_name_")]
    race_cols = [col for col in df.columns if col.startswith("race_name_")]

    features += driver_cols + race_cols

    X = df[features]
    y = df["won_race"]

    return X, y


# Train the model
def train_model(X, y):
    # Split data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Create a pipeline with standardization and logistic regression
    model = make_pipeline(
        StandardScaler(),
        LogisticRegression(class_weight="balanced", max_iter=1000, random_state=42),
    )

    # Train the model
    model.fit(X_train, y_train)

    # Evaluate on test set
    y_pred = model.predict(X_test)
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.2f}")
    print(classification_report(y_test, y_pred))

    return model


# Function to predict race outcome for a specific driver and race
def predict_race_winner(model, driver_name, race_name, df):
    # Create a row with the same structure as training data
    # We'll use median values for numerical features as defaults
    # In a real application, you'd want to use actual recent data for the driver
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
    if driver_name not in pilotes_2025:
        raise ValueError("The driver must participate in the 2025 season.")

    # Create a dictionary with all features set to 0 initially
    input_data = {col: 0 for col in model.feature_names_in_}

    # Set the driver and race columns
    driver_col = f"driver_name_{driver_name}"
    race_col = f"race_name_{race_name}"

    if driver_col not in input_data:
        print(f"Warning: Driver {driver_name} not found in training data")
        return False
    if race_col not in input_data:
        print(f"Warning: Race {race_name} not found in training data")
        return False

    input_data[driver_col] = 1
    input_data[race_col] = 1

    # Set numerical features to median values from training data
    numerical_features = [
        "grid",
        "positionN1",
        "positionN2",
        "positionN3",
        "averageTimeCircuit",
        "positionCircuitN1",
        "positionCircuitN2",
        "positionCircuitN3",
    ]

    for feat in numerical_features:
        if feat in input_data:
            input_data[feat] = df[feat].median()

    # Convert to DataFrame
    input_df = pd.DataFrame([input_data])

    # Ensure columns are in the same order as training data
    input_df = input_df[model.feature_names_in_]

    # Make prediction
    prediction = model.predict(input_df)
    probability = model.predict_proba(input_df)[0][1]

    return bool(prediction[0]), probability


# Main workflow
if __name__ == "__main__":
    # Preprocess the data
    X, y = preprocess_data(data)

    # Train the model
    model = train_model(X, y)

    # Example prediction
    race = "Suzuka Circuit"

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

    print(f"Course: {race} \n")
    driver_probs = []
    for driver in pilotes_2025:
        will_win, probability = predict_race_winner(model, driver, race, data)
        driver_probs.append((driver, will_win, probability))

    # Sort by probability descending
    driver_probs.sort(key=lambda x: x[2], reverse=True)

    for driver, will_win, probability in driver_probs:
        print("------\n")
        print(driver)
        print(f"{will_win}: {probability:.4f}")
