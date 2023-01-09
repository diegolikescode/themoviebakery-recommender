import pandas
import json
import time

overall_time = time.time()
counter = 0

unique_movies_file = open('official-movies-unique.json')
# unique_movies_file = open('sample-movies-rating.json')
unique_movies = json.load(unique_movies_file)

df_rating = pandas.read_csv('ratings.csv')
df_rating.drop('timestamp', inplace=True, axis=1)

for movie in unique_movies:
    start_time = time.time()
    df_rating.loc[df_rating['movieId'] == movie['kaggle_id'], ['movieId']] = movie['id']
    # df_rating.to_csv('official-rating-movies.csv')

    counter += 1
    # if counter % 1000 == 0:
    #     df_rating.to_csv('official-rating-movies.csv')

    print('{}--- {} seconds ---, n {}'.format(movie['title'], (time.time() - start_time), counter))

to_csv_time = time.time()
print('starting to_csv process')
df_rating.to_csv('official-rating-movies.csv')
print('--- %s to_csv seconds ---' % (time.time() - to_csv_time))

unique_movies_file.close()
print('--- %s overall seconds ---' % (time.time() - overall_time))





    # print(movie['title'])
    # for index, row in df_rating.iterrows():
    #     if row[1] == movie['kaggle_id']:
    #         df_rating.loc[index, ['movieId']] = movie['id']
    #         if row[2] < 3:
    #             df_rating.loc[index, ['rating']] = -1
    #         else:
    #             df_rating.loc[index, ['rating']] = 1
