import pandas as pd
from collections import Counter
import requests
import json
import os

dirname = os.path.dirname(__file__)

ratings_local = pd.read_csv(os.path.join(
    dirname, '../../data/data-for-analysis/ratings-smaller-with-new-ids.csv'))

req_ratings = requests.get(
    'http://localhost:8080/api/v1/rating/get-all').json()
json_list = json.dumps(req_ratings, indent=4)

ratings_db = pd.read_json(json_list)
ratings_db.drop(axis=1, labels=['created_at',
                'updated_at', 'ratingId'], inplace=True)
ratings_db.rename(columns={'ratingValue': 'rating'}, inplace=True)
ratings_db['userId'] += 499

ratings_df = pd.concat([ratings_local, ratings_db])
ratings_df.to_csv(os.path.join(
    dirname, '../../data/data-for-analysis/ratings-small-with-database.csv'), index=False)
