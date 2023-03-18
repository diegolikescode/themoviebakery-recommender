import requests
import json
import time

# url = 'https://api.themoviedb.org/3/trending/movie/day?api_key=48386eaa3dee4ec50e05f2aa35c88167&page='
url = 'https://api.themoviedb.org/3/trending/movie/day?api_key=48386eaa3dee4ec50e05f2aa35c88167&page='

page = 1
movies_arr = []
for _ in range(999):
    str_page = str(page)
    # full_url = url+str_page
    res = requests.get(url+str_page)
    json_data = json.loads(res.text)
    # json_str = str(json_data)

    # i = 0
    for i in range(19):
        new_movie = json_data['results'][i]
        movies_arr.append(new_movie)

        i += 1
    print(page)
    page += 1
    time.sleep(0.2)

data = []
with open('tmdb-movies.json', 'w') as file:
    data.extend(movies_arr)
    json.dump(data, file)
