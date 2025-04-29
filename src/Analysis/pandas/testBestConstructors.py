from random import seed
from src.Analysis.pandas import BestConstructors

seed(42)

test_df = BestConstructors.jointure.sample(n=30, random_state=1)
