preparation:
	cd src/data_preparation && python3 a_intersection_movie_dfs.py && python3 b_intersection_ratings_movies.py && cd ..

preprocessing:
	cd src/data_preprocessing && python3 a_shrink_ratings.py && python3 b_userandmovie_newId.py && python3 c_add_database_to_ratings.py && python3 d_data_to_dict.py

full: preparation preprocessing
	python3 src/server.py

only-server:
	python3 src/server.py
