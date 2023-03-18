import pandas as pd
import numpy as np

# userId,movieId,rating,newMovieId
df = pd.read_csv('../data/edited_ratings.csv', usecols=['userId', 'movieId', 'rating'], dtype={
                 'userId': 'string', 'movieId': 'string', 'rating': 'float64'})

unique_user_ids = df.userId.unique()
unique_users_count = {}
c = 0

temp_df = df.copy()
for unique_id in unique_user_ids:
    qnt = len(temp_df[temp_df['userId'] == unique_id])
    if qnt >= 30:
        unique_users_count[unique_id] = qnt
    temp_df = temp_df[temp_df['userId'] != unique_id]

    c += 1
    print('PROGRESS >>>', c, '/', len(unique_user_ids),
          '| ratings_df size:', len(temp_df))

new_df = df[df['userId'].isin(unique_users_count.keys())]

print('FULL DF LEN', len(df))
print('NEW DF LEN', len(new_df))

new_df.to_csv('../data2/ratings_smaller_less_than.csv', index=False)
