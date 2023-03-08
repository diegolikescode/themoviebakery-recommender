# EACH MOVIE HAS 100 REVIEWS
import pandas as pd
import json

movies_json = open('movies.json')
all_movies = json.load(movies_json)

ratings_csv = pd.read_csv('temp.csv', usecols=['userId', 'movieId', 'rating'], dtype={
    'userId': 'string', 'movieId': 'string', 'ratings': 'int8'})

print(len(all_movies))
print(ratings_csv.shape[0])

movie_qnt = 7457
total = 0

# print(ratings_csv.head())
# df = ratings_csv[str(all_movies[0]['id']) == ratings_csv['movieId']]
# print(df)

# full_df = pd.concat([csv_df, json_df]) << concat dataframes
all_dfs = []
for num in range(movie_qnt):
    total += 1
    new_df = ratings_csv[str(all_movies[num]['id']) == ratings_csv['movieId']]
    print('TOTAL NOW >>> ', str(total)+'/'+str(movie_qnt))
    all_dfs.append(new_df.head(100))
    # if new_df.shape[0] < 100:
    #     print(new_df.head(100))
    #     i += 1
    #     print(all_movies[num]['title'] + '  ' +
    #           str(new_df.shape[0]) + '    ' + str(i))

full_df = pd.concat(all_dfs)
full_df.to_csv('temp70.csv', index=False)
