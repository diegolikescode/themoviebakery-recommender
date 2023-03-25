import pandas as pd

ratings_df = pd.read_csv('../../data/data-for-analysis/ratings-smaller-with-new-ids.csv')

print(ratings_df.shape)
print('UNIQUES')
print(ratings_df['newUserId'].unique())
print(ratings_df['newMovieId'].unique())
