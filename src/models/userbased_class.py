import pickle
import numpy as np
from sortedcontainers import SortedList

class user_based_model():
    user2movie = {}
    movie2user = {}
    usermovie2ratings = {}
    usermovie2ratings_test = {}

    K = 25
    limit = 5
    neighbors = []
    averages = []
    deviations = []

    train_predictions = []
    train_targets = []

    test_predictions = []
    test_targets = []

    def __init__(self):
        with open('../../data/data-for-analysis/bin/user2movie.json', 'rb') as file:
            self.user2movie = pickle.load(file)

        with open('../../data/data-for-analysis/bin/movie2user.json', 'rb') as file:
            self.movie2user = pickle.load(file)

        with open('../../data/data-for-analysis/bin/usermovie2ratings.json', 'rb') as file:
            self.usermovie2ratings = pickle.load(file)

        with open('../../data/data-for-analysis/bin/usermovie2ratings_test.json', 'rb') as file:
            self.usermovie2ratings_test = pickle.load(file)

    def calculate_user_neighbors(self):
        N = np.max(list(self.user2movie.keys())) + 1

        m1 = np.max(list(self.movie2user.keys())) + 1
        m2 = np.max([m for (u, m), r in self.usermovie2ratings_test.items()])
        M = max(m1, m2) + 1

        print('N:', N, 'M: ', M)

        key_errs = 0
        count = 0
        for i in range(N):
            try:
                movies_i = self.user2movie[i]
                movie_i_set = set(movies_i)

                ratings_i = {movie: self.usermovie2ratings[(
                    i, movie)] for movie in movies_i}
                avg_i = np.mean(list(ratings_i.values()))
                dev_i = {movie: (rating - avg_i)
                         for movie, rating in ratings_i.items()}
                dev_i_values = np.array(list(dev_i.values()))
                sigma_i = np.sqrt(dev_i_values.dot(dev_i_values))

                self.averages.append(avg_i)
                self.deviations.append(dev_i)

                sortedList = SortedList()
                for j in range(N):
                    if j != i:
                        try:
                            movies_j = self.user2movie[j]
                            movies_j_set = set(movies_j)

                            common_movies = (movie_i_set & movies_j_set)
                            if len(common_movies) > self.limit:
                                ratings_j = {movie: self.usermovie2ratings[(
                                    j, movie)] for movie in movies_j}

                                avg_j = np.mean(list(ratings_j.values()))
                                dev_j = {
                                    movie: (rating - avg_j) for movie, rating in ratings_j.items()
                                }

                                dev_j_values = np.array(list(dev_j.values()))
                                sigma_j = np.sqrt(
                                    dev_j_values.dot(dev_j_values))

                                numerator = sum(dev_i[m] * dev_j[m]
                                                for m in common_movies)
                                w_ij = float(numerator) / (sigma_i * sigma_j)

                                sortedList.add((-w_ij, j))
                                if len(sortedList) > self.K:
                                    del sortedList[-1]
                        except KeyError:
                            key_errs += 1
                            pass

                self.neighbors.append(sortedList)
                count += 1
                print(N, '|', count)
            except KeyError:
                print('KeyError', i)
                pass

    def predict(self, i, m):
        numerator = 0
        denominator = 0

        print('I INSIDE PREDICT', i)
        for neg_w, j in self.neighbors[i]:
            try:
                numerator += -neg_w * self.deviations[j][m]
                denominator += abs(neg_w)
            except KeyError:
                pass

        if denominator == 0:
            prediction = self.averages[i]
        else:
            prediction = numerator / denominator + self.averages[i]

        prediction = min(5, prediction)
        prediction = max(0.5, prediction)
        return prediction

    def train_and_test(self):
        for (i, m), target in self.usermovie2ratings.items():
            prediction = self.predict(i, m)

            self.train_predictions.append(prediction)
            self.train_targets.append(target)

        for (i, m), target in self.usermovie2ratings_test.items():
            prediction = self.predict(i, m)

            self.test_predictions.append(prediction)
            self.test_targets.append(target)

    def calculate_mse(self, p, t):
        p = np.array(p)
        t = np.array(t)
        return np.mean((p - t)**2)

    def predict_for_user(self, user_id):
        user_id = 500
        movies = self.movie2user.keys()

        for mov in movies:
            pred = self.predict(i=user_id, m=mov)
            print(pred)


def doit():
    bravo = user_based_model()
    print('calculating_user_neighbors')
    bravo.calculate_user_neighbors()
    print('training_and_testing')
    bravo.train_and_test()
    print('calculating_mse')
    training_mse = bravo.calculate_mse(
        bravo.train_predictions, bravo.train_targets)
    testing_mse = bravo.calculate_mse(
        bravo.test_predictions, bravo.test_targets)

    print('TRAINING MSE:', training_mse)
    print('TESTING MSE:', testing_mse)

    bravo.predict_for_user(user_id=4)


doit()
