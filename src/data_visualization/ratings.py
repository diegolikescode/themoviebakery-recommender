import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


ratings_raw_df = pd.read_csv('../../data/raw-data/kaggle-ratings.csv')
list_ratings_raw = np.sort(ratings_raw_df['rating'].unique(), kind='quicksort')
raw_list_values = {}
for rating_val in list_ratings_raw:
    raw_list_values[rating_val] = ratings_raw_df[ratings_raw_df['rating']
                                                 == rating_val]['rating'].count()

fig = plt.figure(figsize=(10, 7))
plt.bar(list(list_ratings_raw), raw_list_values.values(), width=0.3)
plt.xlabel('notas de avaliação disponíveis')
plt.ylabel('distribuição das notas')
plt.show()


ratings_full_df = pd.read_csv('../../data/treated-data/all-ratings.csv')
list_ratings = np.sort(ratings_full_df['rating'].unique(), kind='quicksort')
list_values = {}
for rating_val in list_ratings:
    list_values[rating_val] = ratings_full_df[ratings_full_df['rating']
                                              == rating_val]['rating'].count()

fig = plt.figure(figsize=(10, 7))
plt.bar(list(list_ratings), list_values.values(), width=0.3)
plt.xlabel('notas de avaliação disponíveis')
plt.ylabel('distribuição das notas')
plt.show()

ratings_smaller = pd.read_csv(
    '../../data/data-for-analysis/ratings-smaller.csv')

list_ratings_smaller = np.sort(
    ratings_smaller['rating'].unique(), kind='quicksort')

list_values_smaller = {}
for rating_val in list_ratings_smaller:

    list_values_smaller[rating_val] = ratings_smaller[ratings_smaller['rating']
                                                      == rating_val]['rating'].count()

fig = plt.figure(figsize=(10, 7))
plt.bar(list(list_ratings_smaller), list_values_smaller.values(), width=0.3)
plt.xlabel('notas de avaliação disponíveis')
plt.ylabel('distribuição das notas')
plt.show()
