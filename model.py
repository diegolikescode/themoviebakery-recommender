from surprise import accuracy
from surprise.model_selection.validation import cross_validate
from surprise.model_selection import train_test_split
from surprise.model_selection import RandomizedSearchCV, GridSearchCV
from surprise.dataset import Dataset
from surprise.reader import Reader
from surprise import SVD
from surprise import KNNBasic
from surprise import KNNWithMeans
from collections import defaultdict
import pandas as pd
from IPython.display import Markdown, display
import pickle
import requests
import json

reader = Reader()


def concat_dataframes():
    # ratings is the static data from the dataset
    # ratings = pd.read_csv('ratings.csv', usecols=['userId', 'movieId', 'rating'], dtype={
    #     "userId": "string", "movieId": "string", "ratings": "int8"})

    # get the data from
    ratings_db = requests.get('http://localhost:8080/api/v1/rating').json()
    json_list = json.dumps(ratings_db, indent=4)

    json_df = pd.read_json(json_list, dtype={
        "userId": "string", "movieId": "string", "ratingValue": "int8"}).rename(columns={'ratingValue': 'rating'})

    csv_df = pd.read_csv('temp.csv', usecols=['userId', 'movieId', 'rating'], dtype={
        "userId": "string", "movieId": "string", "ratings": "int8"})

    full_df = pd.concat([csv_df, json_df])
    return full_df


full_df = concat_dataframes()

surprise_data = Dataset.load_from_df(full_df, reader)
trainset, testset = train_test_split(
    surprise_data, test_size=.3, random_state=10)


def printmd(string, color=None):
    colorstr = "<span style='color:{}'>{}</span>".format(color, string)
    display(Markdown(colorstr))


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

    def fit_and_predict(self):
        printmd('**Fitting the train data...**', color='brown')
        self.model.fit(self.trainset)

        printmd('**Predicting the test data...**', color='brown')
        self.pred_test = self.model.test(self.testset)
        rmse = round(accuracy.rmse(self.pred_test), 3)
        printmd('**RMSE for the predicted result is ' +
                str(rmse) + '**', color='brown')

        self.top_n = get_top_n(self.pred_test)

        self.recommenddf = pd.DataFrame(
            columns=['userId', 'movieId', 'rating'])
        for item in self.top_n:
            subdf = pd.DataFrame(self.top_n[item], columns=[
                                 'movieId', 'rating'])
            subdf['userId'] = item
            cols = subdf.columns.tolist()
            cols = cols[-1:] + cols[:-1]
            subdf = subdf[cols]
            self.recommenddf = pd.concat([self.recommenddf, subdf], axis=0)
        return rmse

    def cross_validate(self):
        printmd('**Cross Validating the data...**', color='brown')
        cv_result = cross_validate(self.model, self.data, n_jobs=-1)
        cv_result = round(cv_result['test_rmse'].mean(), 3)
        printmd('**Mean CV RMSE is ' + str(cv_result) + '**', color='brown')
        return cv_result

    def recommend(self, user_id, n=5):
        printmd('**Recommending top ' + str(n) +
                ' movies for userid : ' + user_id + ' ...**', color='brown')

        df = pd.DataFrame(self.top_n[user_id], columns=['movieId', 'rating'])
        df['UserId'] = user_id
        cols = df.columns.tolist()
        cols = cols[-1:] + cols[:-1]
        df = df[cols].head(n)
        # df = self.recommenddf[self.recommenddf['userId'] == user_id].head(n)
        display(df)
        return df


def find_best_model(model, parameters, data):
    # clf = RandomizedSearchCV(
    #     model, parameters, n_jobs=-1, measures=['rmse', 'mae'])

    clf = GridSearchCV(
        model, parameters, n_jobs=-1, measures=['rmse', 'mae'])

    clf.fit(data)
    print(clf.best_score)
    print(clf.best_params)
    print(clf.best_estimator)
    return clf


def init_knn_basic():
    params = {
        'n_epochs': [5, 10, 15, 20],
        'lr_all': [0.002, 0.005],
        'reg_all': [0.4, 0.6],
        'sim_options': {
            'user_based': [True]
        }
    }
    clf = find_best_model(KNNBasic, params, surprise_data)

    basic = clf.best_estimator['rmse']
    model_basic = collaborative_filtering_recommender_model(
        basic, trainset, testset, surprise_data)

    model_basic.fit_and_predict()
    model_basic.cross_validate()
    # pickle.dump(model_basic, open('model.pkl', 'wb'))

    ratings_db = requests.get(
        'localhost:8080/api/v1/rating-by-user?userId=GJ7rXUbap').json()
    user_ratings = json.dumps(ratings_db, indent=4)

    watched = []
    for rate in user_ratings:
        watched.append(rate['movieId'])



    # EXAMPLES OF HOW TO CALL THE MODEL
    model_basic.recommend(user_id='GJ7rXUbap', n=20)
    # result_basic_user1 = model_basic.recommend(user_id='1554', n=50)


def init_svd():
    params = {
        'n_epochs': [5, 10, 15, 20],
        'lr_all': [0.002, 0.005],
        'reg_all': [0.4, 0.6],
        'sim_options': {
            'user_based': True
        }
    }
    clf = find_best_model(SVD, params, surprise_data)

    svd = clf.best_estimator['rmse']
    model_svd = collaborative_filtering_recommender_model(
        svd, trainset, testset, surprise_data)

    model_svd.fit_and_predict()
    model_svd.cross_validate()
    # pickle.dump(model_svd, open('model.pkl', 'wb'))

    ratings_db = requests.get(
        'localhost:8080/api/v1/rating-by-user?userId=GJ7rXUbap').json()
    user_ratings = json.dumps(ratings_db, indent=4)

    watched = []
    for rate in user_ratings:
        watched.append(rate['movieId'])

    # EXAMPLES OF HOW TO CALL THE MODEL
    # model_svd.recommend(user_id='GJ7rXUbap', n=20)
    # result_svd_user1 = model_svd.recommend(user_id='1554', n=50)


def init_knn_with_means():
    sim_options = {
        "name": ["msd", "cosine", "pearson", "pearson_baseline"],
        "min_support": [3, 4, 5],
        "user_based": [True],
    }
    params = {'k': range(30, 50, 1), 'sim_options': sim_options}
    clf = find_best_model(KNNWithMeans, params, surprise_data)

    knnwithmeans = clf.best_estimator['rmse']
    model_knnmeans = collaborative_filtering_recommender_model(
        knnwithmeans, trainset, testset, surprise_data)

    model_knnmeans.fit_and_predict()
    model_knnmeans.cross_validate()

    pickle.dump(model_knnmeans, open('model.pkl', 'wb'))

    # EXAMPLES OF HOW TO CALL THE MODEL
    # result_svd_user1 = model_svd.recommend(user_id='1554', n=50)


# init_knn_with_means()
init_svd()
init_knn_basic()
