import pandas as pd

df = pd.read_csv('../data2/ratings_small_newMovieId.csv')

print(df[df['newMovieId'] == float('nan')])
