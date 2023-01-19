import pandas
import numpy as np

df = pandas.read_csv('ratings-that-works.csv',
                     usecols=['userId', 'movieId', 'rating'])

print((df.rating > 2.5).sum())
print((df.rating <= 2.5).sum())

print(df.head())

# df.loc[(df.rating > float(2.5)), 'rating'] = True
# df.loc[(df.rating <= float(2.5)), 'rating'] = False
df['rating'] = np.where(df['rating'] > 2.5, 5, 1)

print('AFTER')
print(df.head())

print((df.rating == 5).sum())
print((df.rating == 1).sum())

df.to_csv('lets-try-this.csv', index=False)
