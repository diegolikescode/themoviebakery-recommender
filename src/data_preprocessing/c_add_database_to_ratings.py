import pandas as pd
from collections import Counter
import requests
import json
import os

dirname = os.path.dirname(__file__)


def add_database():
    ratings_local = pd.read_csv(
        os.path.join(
            dirname,
            '../../data/data-for-analysis/ratings-smaller-with-new-ids.csv'))

    req_ratings = requests.get(
        # 'http://localhost:8080/api/v1/rating/get-all').json()
        'https://www.backend.themoviebakery.com/api/v1/rating/get-all').json()

    json_list = json.dumps(req_ratings, indent=4)

    ratings_db = pd.read_json(json_list)
    if len(ratings_db) != 0:
        ratings_db.drop(axis=1,
                        labels=['created_at', 'updated_at', 'ratingId'],
                        inplace=True)
        ratings_db.rename(columns={'ratingValue': 'rating'}, inplace=True)
        ratings_db['userId'] += 49

        ratings_df = pd.concat([ratings_local, ratings_db])
        ratings_df.to_csv(os.path.join(
            dirname,
            '../../data/data-for-analysis/ratings-small-with-database.csv'),
            index=False)
    else:
        ratings_local.to_csv(os.path.join(
            dirname,
            '../../data/data-for-analysis/ratings-small-with-database.csv'),
            index=False)

    del req_ratings
    del json_list
    del ratings_db


add_database()
