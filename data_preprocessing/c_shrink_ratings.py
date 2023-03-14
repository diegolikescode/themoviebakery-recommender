import pandas as pd
from collections import Counter

ratings_df = pd.read_csv('../data/ratings_new_user_ids.csv')
print('original ratings_df size:', len(ratings_df))

N = ratings_df.newUserId.max() + 1  # user qnt
M = ratings_df.newMovieId.max() + 1 # movies qnt

user_ids_count = Counter(ratings_df.newUserId)
movie_ids_count = Counter(ratings_df.newMovieId)

n = 10000 # qnt of users we want
m = 2000  # qnt of movies we want

user_ids = [u for u, _ in user_ids_count.most_common(n)]
movie_ids = [m for m, _ in user_ids_count.most_common(m)]

ratings_small_df = ratings_df[ratings_df.newUserId.isin(user_ids) & ratings_df.newMovieId.isin(movie_ids)].copy()

new_user_id_map = {}
i = 0
for old in user_ids:
    new_user_id_map[old] = i
    i += 1
print('i:', i)

new_movie_id_map = {}
j = 0
for old in movie_ids:
    new_movie_id_map[old] = j
    j += 1
print('j:', j)

print('setting new ids')
ratings_small_df.loc[:, 'newUserId'] = ratings_small_df.apply(lambda row: new_user_id_map[row.newUserId], axis=1)
ratings_small_df.loc[:, 'newMovieId'] = ratings_small_df.apply(lambda row: new_movie_id_map[row.newMovieId], axis=1)

print ('small ratings df size:', len(ratings_small_df))
ratings_small_df.to_csv('../data/rating_small.csv', index=False)
