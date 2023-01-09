# remAnother,remAgain,rem,isInTmdb
import pandas

df = pandas.read_csv('official-ratings-cleaned.csv')
new_df = df.drop(['remAnother', 'remAgain', 'rem', 'isInTmdb'], axis=1)
new_df.to_csv('_indeed_rating.csv', index=False)

print('DONE!')
