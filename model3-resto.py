from surprise import KNNBasic
from surprise import Dataset
from surprise import Reader

from collections import defaultdict
from operator import itemgetter
import heapq

import requests
import json

import pandas as pd

df = pd.read_csv('temp.csv', usecols=['userId', 'movieId', 'rating'], dtype={
    'userId': 'string', 'movieId': 'string', 'ratings': 'int8'})

# ratings_db = requests.get('http://localhost:8080/api/v1/rating').json()

ratings_db = requests.get(
    'http://localhost:8080/api/v1/rating-by-user?userId=GJ7rXUbap').json()

user_ratings = json.dumps(ratings_db, indent=4)

watched = []
for rate in user_ratings:
    watched.append(rate['movieId'])

reader = Reader()
dataset = Dataset.load_from_df(df, reader=reader)

trainset = dataset.build_full_trainset()

similarity_matrix = KNNBasic(sim_options={
    'name': 'cosine',
    'user_based': True
}).fit(trainset).compute_similarities()

test_subject = 'GJ7rXUbap'
k = 20

test_subject_iid = trainset.to_inner_uid(test_subject)

test_subject_ratings = trainset.ur[test_subject_iid]
k_neighbors = heapq.nlargest(k, test_subject_ratings, key=lambda t: t[1])

candidates = defaultdict(float)

for movieId, rating in k_neighbors:
    try:
        similaritities = similarity_matrix[int(movieId)]
        for innerID, score in enumerate(similaritities):
            candidates[innerID] += score * (rating / 5.0)
    except:
        continue


recommendations = []

position = 0
for movieId, rating_sum in sorted(candidates.items(), key=itemgetter(1), reverse=True):
    if not movieId in watched:
        recommendations.append(movieId)
        position += 1
        if (position > 10):
            break

for rec in recommendations:
    print("Movie: ", rec)
