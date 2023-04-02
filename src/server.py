import numpy as np
from flask import Flask, request, jsonify
import pickle
from models.userbased_class import user_based_model
import data_preprocessing.a_shrink_ratings
import data_preprocessing.b_userandmovie_newId
import data_preprocessing.c_add_database_to_ratings
import data_preprocessing.d_data_to_dict


app = Flask(__name__)
recommender = user_based_model()


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

start_model()

@app.route('/api', methods=['GET'])
def recommend():
    user_id = int(request.args.get('userId'))
    print(user_id)
    recommendations = recommender.recommend_movies_for_users(user_id)

    return jsonify(recommendations)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
