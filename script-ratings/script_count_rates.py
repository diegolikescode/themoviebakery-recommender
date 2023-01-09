import pandas

df = pandas.read_csv('official-rate-movie-checkup.csv')
print(df['isInTmdb'].value_counts())

# True     15_702_991
# False     9_297_104
