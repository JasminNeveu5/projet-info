import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from options.config import DATA_DIR
data = pd.read_csv(f"{DATA_DIR}/df.csv")
data.dropna(inplace = True)
# Encodage des varijables catégorielles
data = pd.get_dummies(data, columns=['driver_name', 'race_name'])
# Séparation des caractéristiques et de la cible
X = data.drop(['isWinner','date','raceId'], axis=1)
y = data["isWinner"]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

model = LogisticRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print(f'Précision du modèle : {accuracy_score(y_test, y_pred)}')

def predire_victoire(pilote, circuit, data, model, scaler):
    # Debugging: Print the original data columns
    print("Original data columns:", data.columns)

    # Créer un DataFrame pour la prédiction avec les colonnes nécessaires
    prediction_data = pd.DataFrame(columns=X.columns)

    # Remplir les colonnes numériques avec les moyennes appropriées
    prediction_data.loc[0, 'positionN1'] = data[(data['driver_name_' + pilote] == 1) & (data['race_name_' + circuit] == 1)]['positionN1'].mean()
    prediction_data.loc[0, 'positionN2'] = data[(data['driver_name_' + pilote] == 1) & (data['race_name_' + circuit] == 1)]['positionN2'].mean()
    prediction_data.loc[0, 'positionN3'] = data[(data['driver_name_' + pilote] == 1) & (data['race_name_' + circuit] == 1)]['positionN3'].mean()
    prediction_data.loc[0, 'positionCircuitN1'] = data[(data['driver_name_' + pilote] == 1) & (data['race_name_' + circuit] == 1)]['positionCircuitN1'].mean()
    prediction_data.loc[0, 'positionCircuitN2'] = data[(data['driver_name_' + pilote] == 1) & (data['race_name_' + circuit] == 1)]['positionCircuitN2'].mean()
    prediction_data.loc[0, 'positionCircuitN3'] = data[(data['driver_name_' + pilote] == 1) & (data['race_name_' + circuit] == 1)]['positionCircuitN3'].mean()
    prediction_data.loc[0, 'positionOrder'] = data[(data['driver_name_' + pilote] == 1) & (data['race_name_' + circuit] == 1)]['positionOrder'].mean()
    prediction_data.loc[0, 'grid'] = data[(data['driver_name_' + pilote] == 1) & (data['race_name_' + circuit] == 1)]['grid'].mean()
    prediction_data.loc[0, 'averageTimeCircuit'] = data[(data['driver_name_' + pilote] == 1) & (data['race_name_' + circuit] == 1)]['averageTimeCircuit'].mean()



    # Remplir les colonnes catégorielles
    prediction_data.loc[0, 'driver_name_' + pilote] = 1
    prediction_data.loc[0, 'race_name_' + circuit] = 1

    # Remplir les colonnes manquantes avec 0
    prediction_data.fillna(0, inplace=True)

    # Debugging: Print prediction data after encoding
    print("Prediction data after encoding:\n", prediction_data)

    # Normalisation des caractéristiques
    prediction_data_scaled = scaler.transform(prediction_data)

    # Prédiction
    prediction = model.predict(prediction_data_scaled)
    probability = model.predict_proba(prediction_data_scaled)[:, 1]  # Probabilité de gagner
    return prediction[0],probability[0]

# Exemple d'utilisation
pilote = 'Max Verstappen'
circuit = 'Monaco Grand Prix'
resultat,probabilite = predire_victoire(pilote, circuit, data, model, scaler)
print(f'Le pilote {pilote} va-t-il gagner sur le circuit {circuit} ? {"Oui" if resultat else "Non"}')
print(f'Probabilité de victoire : {probabilite:.2f}')

