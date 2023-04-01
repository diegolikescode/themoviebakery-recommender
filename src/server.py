import numpy as np
from flask import Flask, request, jsonify
import pickle
import models.userbased_class

app = Flask(__name__)
recommender = models.userbased_class()


def start_model():
    # recommender = user_based_model()
    print('calculating_user_neighbors')
    recommender.calculate_user_neighbors()
    print('training_and_testing')
    recommender.train_and_test()
    print('calculating_mse')
    training_mse = recommender.calculate_mse(
        recommender.train_predictions, recommender.train_targets)
    testing_mse = recommender.calculate_mse(
        recommender.test_predictions, recommender.test_targets)


    # recommender.predict_for_user(user_id=4)

    print('TRAINING MSE:', training_mse)
    print('TESTING MSE:', testing_mse)


@app.route('/api', methods=['GET'])
def recommend():
    user_id = request.args.get('userId')
    print(user_id)
    recommendations = modo.recommend(user_id, n=50)

    movies_arr = []
    for _, row in recommendations.iterrows():
        movies_arr.append(row['movieId'])
        print(row['movieId'])

    return jsonify(movies_arr)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
