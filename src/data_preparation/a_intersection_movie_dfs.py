# script to intersect TMDB movies and Kaggle's Movielens dataset
import pandas as pd
import json
import requests

# tmdb_movies_file = open('../../data/raw-data/tmdb-movies.json')
tmdb_movies_file = requests.get('https://bucket-recommender.s3.us-east-1.amazonaws.com/tmdb-movies.json', headers={'Accept': 'application/json'})
tmdb_movies = tmdb_movies_file.json()
# tmdb_movies_file_pandas = 'https://bucket-recommender.s3.us-east-1.amazonaws.com/tmdb-movies.json'

# kaggle_movies_file = requests.get('https://bucket-recommender.s3.us-east-1.amazonaws.com/kaggle-movies.csv')
kaggle_movies_file = 'https://bucket-recommender.s3.us-east-1.amazonaws.com/kaggle-movies.csv'
# kaggle_movies = pd.read_csv('../../data/raw-data/kaggle-movies.csv')
kaggle_movies = pd.read_csv(kaggle_movies_file)

kaggle_movies['title'] = kaggle_movies.apply(
    lambda row: row[1][slice(len(row[1]) - 7)], axis=1)

c = 0
count_finded = 0
for tmdb_movie in tmdb_movies:
    try:
        c += 1
        kaggleId = kaggle_movies[
            kaggle_movies['title'] == tmdb_movie['title']]['movieId'].values[0]
        print(len(tmdb_movies) - c)
        tmdb_movie['kaggleId'] = int(kaggleId)
        count_finded += 1
    except:
        pass

print('INTERSECTION MOVIES', count_finded)
filtered_movies_list = []
for movie_index, movie in enumerate(tmdb_movies):
    if 'kaggleId' in movie.keys():
        filtered_movies_list.append(movie)


with open('../../data/semi-treated-data/movies_kaggleId.json', 'w') as output_file:
    json.dump(filtered_movies_list, output_file)

tmdb_movies_file.close()
