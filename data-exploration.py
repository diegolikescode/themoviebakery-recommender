import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import requests
import json

df_csv = pd.read_csv('ratings-temp.csv')
ratings_db = requests.get('http://localhost:8080/api/v1/rating').json()
json_list = json.dumps(ratings_db, indent=4)

df_json = pd.read_json(json_list, dtype={
    "userId": "string", "movieId": "string", "ratingValue": "int8"}).rename(columns={'ratingValue': 'rating'})

full_df = pd.concat([df_csv, df_json])
