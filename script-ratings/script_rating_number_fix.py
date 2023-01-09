import pandas

df = pandas.read_csv('_indeed_rating.csv')
df.loc[(df['rating'] >= 3), ['rating']] = 1
df.loc[(df['rating'] < 3), ['rating']] = -1

# print(df.head())

df.to_csv('_this-is-rating.csv', index=False)
