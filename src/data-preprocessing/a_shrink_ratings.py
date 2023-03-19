import pandas as pd
from collections import Counter

ratings_df = pd.read_csv('../../data/treated-data/all-ratings.csv')
print('original ratings_df size:', len(ratings_df))

N = ratings_df.userId.max() + 1  # user qnt
M = ratings_df.movieId.max() + 1 # movies qnt

print('ORIGINAL USER QNT:', N)
print('ORIGINAL MOVIES QNT:', M)

user_ids_count = Counter(ratings_df.userId)
movie_ids_count = Counter(ratings_df.movieId)

n = 2000 # qnt of users we want
m = 500  # qnt of movies we want

user_ids = [u for u, _ in user_ids_count.most_common(n)]
movie_ids = [m for m, _ in user_ids_count.most_common(m)]

ratings_small_df = ratings_df[ratings_df.userId.isin(user_ids) & ratings_df.movieId.isin(movie_ids)].copy()

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
ratings_small_df.loc[:, 'userId'] = ratings_small_df.apply(lambda row: new_user_id_map[row.userId], axis=1)
ratings_small_df.loc[:, 'movieId'] = ratings_small_df.apply(lambda row: new_movie_id_map[row.movieId], axis=1)

print ('small ratings df size:', len(ratings_small_df))
ratings_small_df.to_csv('../../data/data-for-analysis/ratings-smaller.csv', index=False)
