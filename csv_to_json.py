import pandas as pd

arq = pd.read_csv('ratings.csv')
arq.to_json('official-movie-rating.json', orient='table', indent=True)
