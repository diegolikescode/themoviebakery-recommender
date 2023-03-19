import pandas as pd
import numpy as np

movies_df = pd.read_json('../data2/movies_newMovieId.json')
ratings_df = pd.read_csv('../data2/rating_small.csv',
                                 usecols=['userId', 'movieId', 'rating'],
                                 dtype={'userId': 'string', 'movieId': 'string', 'ratings': 'float64'}).head(40)

arr = [0] * len(movies_df)
for i in range(len(arr)):
    arr[i] = i
movies_df['newMovieId'] = arr

ratings_df['newMovieId'] = 0

for index, row in movies_df.iterrows():
    for index2, row_rating in ratings_df.iterrows():
        if(row['id'] == row_rating['movieId']):
            print('OH YES', row_rating['movieId'])
    # ratings_df['newMovieId'] = np.where(ratings_df['movieId'] == row['id'], 50, ratings_df['newMovieId'])
    # ratings_df.loc[ratings_df['movieId'] == str(row['id']),
    #                'newMovieId'] = row['newMovieId']
    print(index, '/', len(movies_df))

print('------------------------------')
# print('AAA GARAI', ratings_df)
print(ratings_df[ratings_df['newMovieId'] == 50])
# movies_dict = movies_df.to_dict('records')
# movies_json = json.dumps(movies_dict, indent=4)
# with open('../data2/movies_newMovieId.json', 'w') as outfile:
#     outfile.write(movies_json)
# ratings_df.to_csv('../data2/ratings_small_newMovieId.csv', index=False)
