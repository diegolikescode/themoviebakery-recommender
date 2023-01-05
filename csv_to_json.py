import pandas as pd

arq = pd.read_csv('ratings.csv')
arq.to_json('kaggle-official-movies.json', orient='table', indent=True)