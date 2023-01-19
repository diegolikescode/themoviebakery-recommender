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

reader = Reader()
ratings = pd.read_csv('sample_ratings.csv')

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
            columns=['userId', 'productId', 'Rating'])
        for item in self.top_n:
            subdf = pd.DataFrame(self.top_n[item], columns=[
                                 'productId', 'Rating'])
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
                ' products for userid : ' + user_id + ' ...**', color='brown')

        #df = pd.DataFrame(self.top_n[user_id], columns=['productId', 'Rating'])
        #df['UserId'] = user_id
        #cols = df.columns.tolist()
        #cols = cols[-1:] + cols[:-1]
        #df = df[cols].head(n)
        df = self.recommenddf[self.recommenddf['userId'] == user_id].head(n)
        display(df)
        return df


def find_best_model(model, parameters, data):
    print('before clf')
    clf = RandomizedSearchCV(model, parameters, n_jobs=-1, measures=['rmse'])
    print('after clf')
    clf.fit(data)
    print(clf.best_score)
    print(clf.best_params)
    print(clf.best_estimator)
    return clf


def init_it():
    sim_options = {
        "name": ["msd", "cosine", "pearson", "pearson_baseline"],
        "min_support": [3, 4, 5],
        "user_based": [True],
    }
    params = {'k': range(30, 50, 1), 'sim_options': sim_options}
    print('here we go')
    clf = find_best_model(KNNWithMeans, params, surprise_data)

    print('not done yet')
    knnwithmeans = clf.best_estimator['rmse']
    col_fil_knnwithmeans = collaborative_filtering_recommender_model(knnwithmeans, trainset, testset, surprise_data)
    print('done!')

    knnwithmeans_rmse = col_fil_knnwithmeans.fit_and_predict()
    knnwithmeans_cv_rmse = col_fil_knnwithmeans.cross_validate()

init_it()
