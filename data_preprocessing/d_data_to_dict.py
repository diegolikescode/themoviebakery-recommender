import pickle
import pandas as pd
from sklearn.utils import shuffle

df = pd.read_csv('../data/rating_small.csv')

N = df.newUserId.max() + 1
M = df.newMovieId.max() + 1

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

    i = int(row.newUserId)
    j = int(row.newMovieId)
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

    i = int(row.newUserId)
    j = int(row.newMovieId)
    usermovie2ratings_test[i, j] = row.rating


df_test.apply(update_usermovie2ratings__test, axis=1)

with open('../bin/user2movie.json', 'wb') as file:
    pickle.dump(user2movie, file)

with open('../bin/movie2user.json', 'wb') as file:
    pickle.dump(movie2user, file)

with open('../bin/usermovie2ratings.json', 'wb') as file:
    pickle.dump(usermovie2ratings, file)

with open('../bin/usermovie2ratings_test.json', 'wb') as file:
    pickle.dump(usermovie2ratings_test, file)
