import numpy as np
from flask import Flask, request, jsonify
import pickle
import model

app = Flask(__name__)
modo = pickle.load(open('model.pkl', 'rb'))


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
