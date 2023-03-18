# script to intersect TMDB movies and Kaggle's Movielens dataset
import pandas as pd

tmdb_movies = pd.read_json('../unprocessed-data/tmdb-movies.json')
print(tmdb_movies.columns)
