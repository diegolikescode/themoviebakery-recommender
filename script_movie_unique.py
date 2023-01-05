import json

official_json = open('official-movies-file.json')
official_data = json.load(official_json)

unique_ones = []

for movie in official_data:
    should_append = True
    for unique in unique_ones:
        if movie['id'] == unique['id']:
            should_append = False
    if should_append:
        unique_ones.append(movie)

print(len(official_data))
print(len(unique_ones))

with open('official-movies-unique.json', 'r') as uniques:
    data = json.load(uniques)

data.append(unique_ones)

with open('official-movies-unique.json', 'w') as uniques:
    json.dump(unique_ones, uniques)

official_json.close()
