import requests
import json
import time

url = 'https://api.themoviedb.org/3/trending/movie/day?api_key=48386eaa3dee4ec50e05f2aa35c88167&page='

page = 1
for _ in range(999):
  str_page = str(page)
  # full_url = url+str_page
  res = requests.get(url+str_page)
  json_data = json.loads(res.text)
  # json_str = str(json_data)

  # print(json_data['results'][0])
  i = 0
  for _ in range(19):
    new_movie = json_data['results'][i]
    with open('only-movies.json', 'r') as file:
      data = json.load(file)
    
    data.append(new_movie)

    with open('only-movies.json', 'w') as file:
      json.dump(data, file)

    i += 1
  print(page)
  page += 1
  time.sleep(10)
