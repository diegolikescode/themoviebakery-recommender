import json

# kaggle_json = open('sample-kaggle.json')
kaggle_json = open('official-movies-kaggle.json')
kaggle_data = json.load(kaggle_json)

# tmdb_json = open('sample-tmdb.json')
tmdb_json = open('official-movies-tmdb.json')
tmdb_data = json.load(tmdb_json)

for movie_kaggle in kaggle_data['data']:
  title_kaggle = movie_kaggle['title'][slice(len(movie_kaggle['title']) - 7)]

  for movie_tmdb in tmdb_data:
    if 'title' in movie_tmdb:
      title_tmdb = movie_tmdb['title']
    else:
      if 'name' in movie_tmdb:
        title_tmdb = movie_tmdb['name']
      else:
        title_tmdb = 'dang!'

    if title_kaggle == title_tmdb:
      print('GOTCHA! '+title_tmdb)
      # estruturar os dados XX, abrir arquivo oficial, acrescentar o filme novo, salvar o arquivo
      movie_tmdb['kaggle_id'] = movie_kaggle['movieId']
      movie_tmdb['genres'] = movie_kaggle['genres']

      with open('official-file.json', 'r') as official_file:
        data = json.load(official_file)

      data.append(movie_tmdb)

      with open('official-file.json', 'w') as official_file:
        json.dump(data, official_file)

      break


kaggle_json.close()
tmdb_json.close()
