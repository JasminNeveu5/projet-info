import pandas as pd

status_code  = pd.read_csv('../../../data/status.csv')
f1_constructor = pd.read_csv('../../../data/constructors.csv')
results = pd.read_csv('../../../data/results.csv')

# === Construction de la table ===

results_x_constructor = pd.merge(results, f1_constructor, on='constructorId')[["constructorId", "statusId"]]

# On compte les occurrences de chaque message d'erreur pour chaque constructeur
status_counts = results_x_constructor.groupby(['constructorId', 'statusId']).size().reset_index(name='count')

# On enlève les statusId qui ne sont pas liés à un défaut de voiture (par exemple "course réussi", ou "pilote malade")
# Ces statusId ont été récupéré à la main en lisant les problèmes qu'ils indiquaient.
status_counts = status_counts[
    ~status_counts['statusId'].isin([1, 2, 3, 4, 31, 50, 128, 53, 58, 73, 81, 82, 88, 97, 100] + list(range(11, 20)))]

# Calculer le total des occurrences de résultats par constructeur (le nombre de courses auxquels ils ont participé)
total_counts = results_x_constructor.groupby('constructorId').size().reset_index(name='total_count')

# Ajouter la colonne de proportion de problèmes dans le tableau
status_counts = pd.merge(status_counts, total_counts, on='constructorId')
status_counts['proportion'] = status_counts['count'] / status_counts['total_count']

# === Problèmes les plus fréquents par constructeur ===


# Trie par 'constructorId' et 'count' (desc), et sélection des 10 principaux status ID par constructeur
status_counts_per_constructor = status_counts.sort_values(by=['constructorId', 'count'], ascending=[True, False])
status_counts_per_constructor = status_counts_per_constructor.groupby('constructorId').head(10)

# Fusion avec la table `status_code` et inclut les noms des constructeurs
status_counts_per_constructor = pd.merge(status_counts_per_constructor, status_code, on='statusId')
status_counts_per_constructor = pd.merge(status_counts_per_constructor, f1_constructor[['constructorId', 'name']], on='constructorId')

# status_counts_per_constructor.drop(["statusId","constructorId"], axis=1, inplace=True)
print(status_counts_per_constructor.head())

# === Constructeurs avec le plus de problèmes ===

# EN NB D'OCCURRENCES
status_counts_constructor = status_counts_per_constructor.groupby('name')[['count','constructorId']].sum().reset_index()

print(status_counts_constructor.sort_values(by='count', ascending=False))

# EN PROPORTION

failures_per_constructor = status_counts_constructor.merge(total_counts, on='constructorId')
failures_per_constructor['failure_proportion'] = failures_per_constructor['count'] / failures_per_constructor[
    'total_count']

# Tri des résultats en ordre décroissant par proportion de pannes
failures_per_constructor_sorted = failures_per_constructor.sort_values(by='failure_proportion', ascending=False)

print(failures_per_constructor_sorted[['name', 'failure_proportion']])
