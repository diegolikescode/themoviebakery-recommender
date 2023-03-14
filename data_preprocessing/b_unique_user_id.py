import pandas as pd

ratings_df = pd.read_csv('../data/edited_ratings.csv')

distinct_user_ids = ratings_df.userId.unique()
count = 0
for id in distinct_user_ids:
    ratings_df.loc[ratings_df['userId'] == id, 'newUserId'] = count
    count += 1
    print('progress:', count, '/', len(distinct_user_ids))

ratings_df.to_csv('../data/ratings_new_user_ids.csv', index=False)
