import pandas as pd

rs = pd.read_json('official-movies-unique.json')

print(len(rs))
# csv: 25_000_095
# jsn: 7_457
# 25_000_095 x 7_457
# 186_425_708_415
