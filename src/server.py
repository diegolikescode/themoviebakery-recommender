from flask import Flask, request, jsonify, json
from flask_cors import CORS
from models.userbased_class import user_based_model

# DATA PREPARATION
from data_preparation.a_intersection_movie_dfs import intersection_movie_dfs
from data_preparation.b_intersection_ratings_movies import intersection_ratings_movies
## 	DATA PREPROCESSING
from data_preprocessing.a_shrink_ratings import shrink_ratings
from data_preprocessing.b_userandmovie_newId import user_movie2new_id
from data_preprocessing.c_add_database_to_ratings import add_database
from data_preprocessing.d_data_to_dict import data_to_dict
import os

dirname = os.path.dirname(__file__)

app = Flask(__name__)

CORS(app,
     origins=['*'],
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
     ],
     supports_credentials=False)

recommender = user_based_model()


def training_model():
    print('calculating_user_neighbors')
    recommender.calculate_user_neighbors()
    print('training_and_testing')
    recommender.train_and_test()
    print('calculating_mse')
    training_mse = recommender.calculate_mse(recommender.train_predictions,
                                             recommender.train_targets)
    testing_mse = recommender.calculate_mse(recommender.test_predictions,
                                            recommender.test_targets)

    print('TRAINING MSE:', training_mse)
    print('TESTING MSE:', testing_mse)


print('training_model')
training_model()


@app.route('/api', methods=['GET'])
def recommend():
    user_id = int(request.args.get('userId'))
    print(user_id)
    recommendations = recommender.recommend_movies_for_users(user_id)

    return jsonify(recommendations)


@app.route('/train', methods=['GET'])
def train():
    intersection_movie_dfs()
    intersection_ratings_movies()
    shrink_ratings()
    user_movie2new_id()
    add_database()
    data_to_dict()
    recommender.reload_files()
    training_model()

    print('TRAIN COMPLETE')
    return jsonify({'message': 'ok'})


if __name__ == '__main__':
    # app.run(port=5000, debug=True, use_reloader=False)
    from waitress import serve
    serve(app, host='0.0.0.0', port=5000)
