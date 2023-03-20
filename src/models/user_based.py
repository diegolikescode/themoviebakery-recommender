import pickle
import numpy as np
from sortedcontainers import SortedList

with open('../../data/data-for-analysis/bin/user2movie.json', 'rb') as file:
    user2movie = pickle.load(file)

with open('../../data/data-for-analysis/bin/movie2user.json', 'rb') as file:
    movie2user = pickle.load(file)

with open('../../data/data-for-analysis/bin/usermovie2ratings.json', 'rb') as file:
    usermovie2ratings = pickle.load(file)

with open('../../data/data-for-analysis/bin/usermovie2ratings_test.json', 'rb') as file:
    usermovie2ratings_test = pickle.load(file)

N = np.max(list(user2movie.keys())) + 1

m1 = np.max(list(movie2user.keys())) # + 1
m2 = np.max([m for (u, m), r in usermovie2ratings_test.items()])
M = max(m1, m2) + 1

print('N:', N, 'M: ', M)

if N > 10_000:
    print("N = ', N, 'O(N) will be very costly")

K = 25
limit = 5
neighbors = []
averages = []
deviations = []

key_errs = 0
for i in range(N):
    movies_i = user2movie[i]
    movie_i_set = set(movies_i)

    ratings_i = {movie: usermovie2ratings[(i, movie)] for movie in movies_i}
    avg_i = np.mean(list(ratings_i.values()))
    dev_i = {movie: (rating - avg_i) for movie, rating in ratings_i.items()}
    dev_i_values = np.array(list(dev_i.values()))
    sigma_i = np.sqrt(dev_i_values.dot(dev_i_values))

    averages.append(avg_i)
    deviations.append(dev_i)

    sortedList = SortedList()
    for j in range(N):
        if j != i:
            try:
                movies_j = user2movie[j]
                movies_j_set = set(movies_j)
                common_movies = (movie_i_set & movies_j_set)  # intersection
                if len(common_movies) > limit:
                    ratings_j = {movie: usermovie2ratings[(
                        j, movie)] for movie in movies_j}

                    avg_j = np.mean(list(ratings_j.values()))
                    dev_j = {
                        movie: (rating - avg_j) for movie, rating in ratings_j.items()
                    }

                    dev_j_values = np.array(list(dev_j.values()))
                    sigma_j = np.sqrt(dev_j_values.dot(dev_j_values))

                    numerator = sum(dev_i[m] * dev_j[m] for m in common_movies)
                    w_ij = float(numerator) / (sigma_i * sigma_j)

                    sortedList.add((-w_ij, j))
                    if len(sortedList) > K:
                        del sortedList[-1]
            except KeyError:
                key_errs += 1
                pass
    print('APPENDING', i, '/', N)
    neighbors.append(sortedList)


def predict(i, m):
    print('PREDICTING')
    numerator = 0
    denominator = 0
    for neg_w, j in neighbors[i]:
        try:
            numerator += -neg_w * deviations[j][m]
            denominator += abs(neg_w)
        except KeyError:
            pass

    if denominator == 0:
        prediction = averages[i]
    else:
        prediction = numerator / denominator + averages[i]

    prediction = min(5, prediction)
    prediction = max(0.5, prediction)
    return prediction


train_predictions = []
train_targets = []
for (i, m), target in usermovie2ratings.items():
    prediction = predict(i, m)
    print(prediction, i, m)
    train_predictions.append(prediction)
    train_targets.append(target)

test_predictions = []
test_targets = []
for (i, m), target in usermovie2ratings_test.items():
    prediction = predict(i, m)

    test_predictions.append(prediction)
    test_targets.append(target)


def mse(p, t):
    p = np.array(p)
    t = np.array(t)
    return np.mean((p - t)**2)


print('train mse: ', mse(train_predictions, train_targets))
print('test mse: ', mse(test_predictions, test_targets))

# with open('user_based_bin_model.py', 'wb') as file:
#     pickle.dump(user_based_model, file)
