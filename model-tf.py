import tensorflow as tf
import tensorflow_datasets as tfds

ratings = tfds.load(name='temp.csv', split='train')
ratings = ratings.map(lambda x: {
    'user_id': x['userId'],
    'movie_id': x['movieId'],
    'rating': x['rating']
})

tf.random.set_seed(42)
shuffled = ratings.shuffle(100_000, seed=42, reshuffle_each_iteration=False)

# train = shuffled.take(?)
# test = shuffled.skip(?).take(?)
