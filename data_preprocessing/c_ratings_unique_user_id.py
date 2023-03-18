import pandas as pd

ratings_df = pd.read_csv('../data2/ratings_small_newMovieId.csv')

ratings_df['newUserId'] = float('nan')

distinct_user_ids = ratings_df.userId.unique()
count = 0
for id in distinct_user_ids:
    ratings_df.loc[ratings_df['userId'] == id, 'newUserId'] = count
    count += 1
    print('progress:', count, '/', len(distinct_user_ids))

ratings_df.to_csv('../data2/ratings_unique_user_ids.csv', index=False)
