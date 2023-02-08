from surprise import accuracy
from surprise.model_selection.validation import cross_validate
from surprise.model_selection import train_test_split
from surprise.model_selection import RandomizedSearchCV
from surprise.dataset import Dataset
from surprise.reader import Reader
from surprise import SVD
from surprise import KNNBasic
from surprise import KNNWithMeans
from collections import defaultdict
import pandas as pd
from IPython.display import Markdown, display
import pickle

reader = Reader()

ratings = pd.read_csv('ratings.csv', usecols=['userId', 'movieId', 'rating'], dtype={
                      "userId": "string", "movieId": "string", "ratings": "int8"})

surprise_data = Dataset.load_from_df(ratings, reader)
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

        #df = pd.DataFrame(self.top_n[user_id], columns=['movieId', 'rating'])
        #df['UserId'] = user_id
        #cols = df.columns.tolist()
        #cols = cols[-1:] + cols[:-1]
        #df = df[cols].head(n)
        df = self.recommenddf[self.recommenddf['userId'] == user_id].head(n)
        display(df)
        return df


def find_best_model(model, parameters, data):
    clf = RandomizedSearchCV(
        model, parameters, n_jobs=-1, measures=['rmse', 'mae'])
    clf.fit(data)
    print(clf.best_score)
    print(clf.best_params)
    print(clf.best_estimator)
    return clf


def init_knn_with_means():
    sim_options = {
        "name": ["msd", "cosine", "pearson", "pearson_baseline"],
        "min_support": [3, 4, 5],
        "user_based": [True],
    }
    params = {'k': range(30, 50, 1), 'sim_options': sim_options}
    clf = find_best_model(KNNWithMeans, params, surprise_data)

    knnwithmeans = clf.best_estimator['rmse']
    col_fil_knnwithmeans = collaborative_filtering_recommender_model(
        knnwithmeans, trainset, testset, surprise_data)

    knnwithmeans_rmse = col_fil_knnwithmeans.fit_and_predict()
    knnwithmeans_cv_rmse = col_fil_knnwithmeans.cross_validate()
    print(knnwithmeans_rmse)
    print(knnwithmeans_cv_rmse)

    # EXAMPLES OF HOW TO CALL THE MODEL
    # result_knn_user1 = col_fil_knnwithmeans.recommend(user_id='ANTN61S4L7WG9', n=5)
    # result_knn_user2 = col_fil_knnwithmeans.recommend(user_id='AYNAH993VDECT', n=5)
    # result_knn_user3 = col_fil_knnwithmeans.recommend(user_id='A18YMFFJW974QS', n=5)


def init_svd():
    params = {
        "n_epochs": [5, 10, 15, 20],
        "lr_all": [0.002, 0.005],
        "reg_all": [0.4, 0.6]
    }
    clf = find_best_model(SVD, params, surprise_data)

    svd = clf.best_estimator['rmse']
    model_svd = collaborative_filtering_recommender_model(
        svd, trainset, testset, surprise_data)

    svd_rmse = model_svd.fit_and_predict()
    # print(svd_rmse)

    svd_cv_rmse = model_svd.cross_validate()
    # print(svd_cv_rmse)
    pickle.dump(model_svd, open('model.pkl', 'wb'))

    # EXAMPLES OF HOW TO CALL THE MODEL
    # result_svd_user1 = model_svd.recommend(user_id='1554', n=50)

    # movies_arr = []
    # for _, row in result_svd_user1.iterrows():
    #     movies_arr.append(row['movieId'])
    #     print(row['movieId'])


# init_knn_with_means()
init_svd()
