#! /env/bin/python

from scikits.crab import datasets
from scikits.crab.metrics import pearson_correlation
from scikits.crab.models import MatrixPreferenceDataModel
from scikits.crab.recommenders.knn import UserBasedRecommender
from scikits.crab.similarities import UserSimilarity

# Get the data
movies = datasets.load_sample_movies()
print type(movies)
for key in movies:
    print key, '\t', movies[key]
print

# Build the model
model = MatrixPreferenceDataModel(movies.data)

# Build the similarity
similarity = UserSimilarity(model, pearson_correlation)

# Build the User based recommender
recommender = UserBasedRecommender(model, similarity, with_preference=True)

# Recommend items for the user
for x in range(1, 6):
    print movies.user_ids[x], recommender.recommend(x)
