import pandas

# True     15_702_991
# False     9_297_104

df = pandas.read_csv('official-rate-movie-checkup.csv')
new_df = df[df.isInTmdb == True]

print(new_df['isInTmdb'].value_counts())
# new_df.drop('isInTmdb', inplace=True, axis=1)

new_df.to_csv('official-ratings-cleaned.csv')
