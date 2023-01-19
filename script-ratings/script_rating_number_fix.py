import pandas

df = pandas.read_csv('rating.csv')
df.loc[(df['rating'] == 1), ['rating']] = True
df.loc[(df['rating'] == -1), ['rating']] = False

print(df.dtypes)

df.to_csv('ratings_bool.csv', index=False)
