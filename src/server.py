import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import pickle
import os
# print('a_shrink_ratings')
# import data_preprocessing.a_shrink_ratings
# print('b_userandmovie_newId')
# import data_preprocessing.b_userandmovie_newId
# print('c_add_database_to_ratings')
# import data_preprocessing.c_add_database_to_ratings
# print('d_data_to_dict')
# import data_preprocessing.d_data_to_dict
from models.userbased_class import user_based_model


app = Flask(__name__)
CORS(app, origins=['*themoviebakery.com*', '*localhost*'],
     methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'],
     allow_headers=[
    'X-CSRF-Token',
    'X-Requested-With',
    'Accept',
    'Accept-Version',
    'Content-Length',
    'Content-MD5',
    'Content-Type',
    'Date',
    'X-Api-Version',
    'Authorization',
], supports_credentials=False)
recommender = user_based_model()


def start_model():
    print('start_model')
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
    # app.run(port=5000, debug=True, use_reloader=False)
    from waitress import serve
    serve(app, host='0.0.0.0', port=5000)
