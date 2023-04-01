# set newMovieId to the ratings dataset
import pandas as pd

ratings_df = pd.read_csv('../../data/data-for-analysis/ratings-smaller.csv')

# TREATING NEW MOVIE ID
# ratings_df['newMovieId'] = ratings_df['movieId'].copy()
# ratings_df.convert_dtypes(convert_floating=True)

# unique_movies = ratings_df['movieId'].unique()
# new_ids = [0] * len(unique_movies)
# movie2newId = {}
# for i in range(len(new_ids)):
#     movie2newId[unique_movies[i]] = i
#     new_ids[i] = i

# ratings_df['newMovieId'].replace(movie2newId, inplace=True)

# TREATING NEW USER ID
unique_users = ratings_df['userId'].unique()
new_ids = [0] * len(unique_users)
user2newId = {}
for i in range(len(new_ids)):
    user2newId[unique_users[i]] = i
    new_ids[i] = i

ratings_df['userId'].replace(user2newId, inplace=True)
ratings_df.to_csv('../../data/data-for-analysis/ratings-smaller-with-new-ids.csv', index=False)
