import pickle
import pandas as pd
from sklearn.utils import shuffle
import os

dirname = os.path.dirname(__file__)

df = pd.read_csv(
    '../../data/data-for-analysis/ratings-small-with-database.csv')

N = df.userId.max() + 1
M = df.movieId.max() + 1

df = shuffle(df)
cutoff = int(0.8*len(df))
df_train = df.iloc[:cutoff]
df_test = df.iloc[cutoff:]

user2movie = {}
movie2user = {}
usermovie2ratings = {}

count = 0


def update_user2movie_and_movie2user(row):
    global count
    count += 1
    if count % 100_000 == 0:
        print('process %.3f' % (float(count)/cutoff))

    i = int(row.userId)
    j = int(row.movieId)
    if i not in user2movie:
        user2movie[i] = [j]
    else:
        user2movie[i].append(j)

    if j not in movie2user:
        movie2user[j] = [i]
    else:
        movie2user[j].append(i)

    usermovie2ratings[(i, j)] = row.rating


df_train.apply(update_user2movie_and_movie2user, axis=1)

usermovie2ratings_test = {}
count = 0


def update_usermovie2ratings__test(row):
    global count
    count += 1
    if count % 100_000 == 0:
        print('process %.3f' % (float(count)/len(df_test)))

    i = int(row.userId)
    j = int(row.movieId)
    usermovie2ratings_test[i, j] = row.rating


df_test.apply(update_usermovie2ratings__test, axis=1)

with open(os.path.join(dirname, '../../data/data-for-analysis/bin/user2movie.json'), 'wb') as file:
    pickle.dump(user2movie, file)

with open(os.path.join(dirname, '../../data/data-for-analysis/bin/movie2user.json'), 'wb') as file:
    pickle.dump(movie2user, file)

with open(os.path.join(dirname, '../../data/data-for-analysis/bin/usermovie2ratings.json'), 'wb') as file:
    pickle.dump(usermovie2ratings, file)

with open(os.path.join(dirname, '../../data/data-for-analysis/bin/usermovie2ratings_test.json'), 'wb') as file:
    pickle.dump(usermovie2ratings_test, file)
