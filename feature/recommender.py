# -------------------
# Recommender Feature
# -------------------
# Defines the feature to generate recommendations from input 
# Defines the feature to build a user profile from inputs 


import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import normalize
from scipy.sparse import csr_matrix
from data_processing.transform import * 


def get_recommendations(list_of_movie_ids, top_n=10):
    # call import scripts and create individual matrices from imported movie data
    keyword_matrix, genre_matrix, collection_matrix, company_matrix, movie_ids = create_matrices()

    # cast all matrices to float
    keyword_matrix = keyword_matrix.astype(float)
    genre_matrix = genre_matrix.astype(float)
    collection_matrix = collection_matrix.astype(float)
    company_matrix = company_matrix.astype(float)

    # combine into one sparse matrix
    combined_matrix = combine_matrices(keyword_matrix, genre_matrix, collection_matrix, company_matrix, [.35, .2, .25, .2] )

    # get a taste profile from the users previous watch history
    user_profile = build_user_profile(list_of_movie_ids, combined_matrix, movie_ids)

    # compute cosine similarity between the user profile and avaliable movies
    similarity_scores = cosine_similarity(user_profile, combined_matrix).flatten()

    # remove previously viewed movies
    exclude = np.isin(movie_ids, list_of_movie_ids)
    similarity_scores[exclude] = 0

    # get top n highest similarity scores
    highest_scores = np.argsort(-similarity_scores)[:top_n]

    # create a dataframe with the results
    recommendations = pd.DataFrame({
        "movie_id": movie_ids[highest_scores],
        "similarity": similarity_scores[highest_scores]
    })
    return recommendations

# creates a single vector that represents the taste profile of a user
def build_user_profile(user_movie_ids, combined_matrix, movie_ids):
    movie_mask = np.isin(movie_ids, user_movie_ids)

    if not np.any(movie_mask):
        raise ValueError("No movie ids input")
    
    user_profile = combined_matrix[movie_mask].mean(axis=0)

    return csr_matrix(user_profile)



