import pandas
import json

unique_movies_file = open('official-movies-unique.json')
unique_movies = json.load(unique_movies_file)

csv_file = pandas.read_csv('ratings.csv')
for index, row in csv_file.iterrows():
    for movie in unique_movies:
        if row[1] == movie['kaggle_id']:
            csv_file.loc[index, ['movieId']] = movie['id']
            if row[2] < 3:
                csv_file.loc[index, ['rating']] = -1
            else:
                csv_file.loc[index, ['rating']] = 1

            print(movie['title'])

csv_file.to_csv('official-rating-movies.csv')

unique_movies_file.close()
