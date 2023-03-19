# set newMovieId to the ratings dataset
import pandas as pd
import numpy as np

# movies = json.load(open('../../data/treated-data/movies_kaggleId.json'))
ratings_df = pd.read_csv('../../data/data-for-analysis/ratings-smaller.csv')
ratings_df['newMovieId'] = ratings_df['movieId'].copy()

unique_movies = ratings_df['movieId'].unique()
new_ids = [0] * len(unique_movies)
movie2newId = {}
for i in range(len(new_ids)):
    movie2newId[unique_movies[i]] = i
    new_ids[i] = i

ratings_df['newMovieId'].replace(movie2newId, inplace=True)

print(ratings_df)
