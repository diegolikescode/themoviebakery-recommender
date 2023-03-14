import pandas as pd

import requests
import json

movies_df = pd.read_json('../data/movies.json')
dataset_ratings_df = pd.read_csv('../data/ratings.csv',
                         usecols=['userId', 'movieId', 'rating'],
                         dtype={'userId': 'string', 'movieId': 'string', 'ratings': 'float64'})

arr = [0] * len(movies_df)
for i in range(len(arr)):
    arr[i] = i
movies_df['newMovieId'] = arr

ratings_db = requests.get('http://localhost:8080/api/v1/rating').json()
json_list = json.dumps(ratings_db, indent=4)

json_df = pd.read_json(json_list, dtype={
    "userId": "string", "movieId": "string", "ratingValue": "float64"}).rename(columns={'ratingValue': 'rating'})

ratings_df = pd.concat([json_df, dataset_ratings_df])


ratings_df['newMovieId'] = 0
ratings_df['newUserId'] = 0

for index, row in movies_df.iterrows():
    ratings_df.loc[ratings_df['movieId'] == str(row['id']),
                   'newMovieId'] = row['newMovieId']
    print(index, '/', len(movies_df))

print('------------------------------')
print(ratings_df)
movies_dict = movies_df.to_dict('records')
movies_json = json.dumps(movies_dict, indent=4)
with open('../data/edited_movies.json', 'w') as outfile:
    outfile.write(movies_json)
ratings_df.to_csv('../data/edited_ratings.csv', index=False)
