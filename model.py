from surprise import accuracy
from surprise.model_selection.validation import cross_validate
from surprise.dataset import Dataset
from surprise.reader import Reader
from surprise import SVD
from surprise import KNNBasic
from surprise import KNNWithMeans
from surprise.model_selection import train_test_split
from collections import defaultdict
import pandas

reader = Reader()
ratings = pandas.read_csv('ratings.csv')

surprise_data = Dataset.load_from_df(ratings, reader)
trainset, testset = train_test_split(surprise_data, test_size=.3, random_state=10)

def get_top_n(predictions, n=10):
    # first map the predictions to each user
    top_n = defaultdict(list)
    for uid, iid, true_r, est, _ in predictions:
        top_n[uid].append((iid, est))

    # then sort predictions for each user and retrieve the k highest ones
    for uid, user_ratings in top_n.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        top_n[uid] = user_ratings[:n]

    return top_n

class collaborative_filtering_recommender_model():
    def __init__(self, model, trainset, testset, data):
        self.model = model
        self.trainset = trainset
        self.testset = testset
        self.data = data
        self.pred_test = None
        self.recommendations = None
        self.top_n = None
        self.recommenddf = None
