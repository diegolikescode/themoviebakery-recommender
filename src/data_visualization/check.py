import pandas as pd

ratings_df = pd.read_csv('../../data/data-for-analysis/ratings-smaller-with-new-ids.csv')
print(len(ratings_df['newUserId'].unique()))