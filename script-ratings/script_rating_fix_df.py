import pandas
import numpy as np

df = pandas.read_csv('official-ratings-cleaned.csv',
                     usecols=['userId', 'movieId', 'rating'])

print((df.rating > 2.5).sum())
print((df.rating <= 2.5).sum())

print(df.head())

# df.loc[(df.rating > float(2.5)), 'rating'] = True
# df.loc[(df.rating <= float(2.5)), 'rating'] = False
df['rating'] = np.where(df['rating'] > 2.5, True, False)

print('AFTER')
print(df.head())

print((df.rating == True).sum())
print((df.rating == False).sum())

df.to_csv('rating_corrected.csv', index=False)
