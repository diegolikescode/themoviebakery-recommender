import pandas

df = pandas.read_csv('sample_ratings.csv')
df.loc[(df['rating'] == 1), ['rating']] = True
df.loc[(df['rating'] == -1), ['rating']] = False

print(df.dtypes)

df.to_csv('new_sample.csv', index=False)
