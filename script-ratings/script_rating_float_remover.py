import math
import pandas

df = pandas.read_csv('ratings_float.csv')
df['rating'] = df['rating'].astype(int)

df.to_csv('rating.csv', index=False)
