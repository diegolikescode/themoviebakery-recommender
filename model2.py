from surprise import accuracy, Dataset, SVD, KNNBasic
from surprise.model_selection import train_test_split, KFold
from surprise.reader import Reader

import requests
import json
import pandas as pd

def concat_dataframes():
    ratings_db = requests.get('http://localhost:8080/api/v1/rating').json()
    json_list = json.dumps(ratings_db, indent=4)

    json_df = pd.read_json(json_list, dtype={
        "userId": "string", "movieId": "string", "ratingValue": "int8"}).rename(columns={'ratingValue': 'rating'})

    csv_df = pd.read_csv('ratings.csv', usecols=['userId', 'movieId', 'rating'], dtype={
        "userId": "string", "movieId": "string", "ratings": "int8"})

    reader = Reader()
    full_df = pd.concat([csv_df, json_df])
    surprise_df = Dataset.load_from_df(df=full_df, reader=reader)
    return surprise_df


data = concat_dataframes()

trainset, testset = train_test_split(data, test_size=0.25)

algo = KNNBasic()

algo.fit(trainset)
predictions = algo.test(testset)

movies_json = json.load(open('movies.json'))

for movie in movies_json:
    res = algo.predict(uid='GJ7rXUbap', iid=str(movie['id']), r_ui=5, verbose=True)
    print(res)
