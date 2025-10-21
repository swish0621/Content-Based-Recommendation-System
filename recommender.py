import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import normalize
from transform import * 


def get_recommendations(list_of_movies_ids):
    # call import scripts and create individual matrices from imported movie data
    keyword_matrix, genre_matrix, collection_matrix, company_matrix, movie_ids = create_matrices()

    # combine into one sparse matrix
    combined_matrix = combine_matrices(keyword_matrix, genre_matrix, collection_matrix, company_matrix)

# creates a single vector that represents the taste profile of a user
def build_user_profile(user_movie_ids, combined_matrix, movie_ids):
    movie_mask = np.isin(movie_ids, user_movie_ids)

    if not np.any(movie_mask):
        raise ValueError("No movie ids input")
    
    user_profile = combined_matrix[movie_mask].mean(axis=0)
    
    return user_profile



