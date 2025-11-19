# ---------------------------------------------------------
# Validation Script for Content-Based-Recommendation-System
# ---------------------------------------------------------
# Evaluates recommendations using Precision@5 metric
# Generates and loads cached similarity matrices
# Tests the validity of recommendations 


from data_processing.transform import combine_matrices, create_matrices
from sklearn.metrics.pairwise import cosine_similarity
from feature.recommender import get_recommendations
import sqlite3
import numpy as np
import os

# Returns movies meeting the similarity threshold of a given movie
def get_relevant_items(index, similarity_matrix, threshold=0.5):
    similarity = similarity_matrix[index]
    return {
        idx for idx, sim in enumerate(similarity)
        if idx != index and sim >= threshold
    }

# Determines how many of the top 5 recommendations are relevant 
def precision_at_5(input_index, recommended_indices, similarity_matrix, threshold=0.5):
    relevant = get_relevant_items(input_index, similarity_matrix, threshold)
    top_5 = recommended_indices[:5]
    valid = sum(1 for rec in top_5 if rec in relevant)
    return valid / 5

# Validates recommendations
# Converts IDs to matrix indices, runs the recommender and scores the recommendations 
def validate(movie_ids_input, movie_ids, similarity_matrix):
    input_indices = [id_to_idx[movie_id] for movie_id in movie_ids_input]

    recommendations = get_recommendations(movie_ids_input)
    recommended_ids = recommendations["movie_id"].tolist()
    
    recommended_indices = [id_to_idx[movie_id] for movie_id in recommended_ids]

    return precision_at_5(input_indices[0], recommended_indices, similarity_matrix)

# Finds a movie by title and validates it
def search_title(title):
    conn = sqlite3.connect("movies.db")
    cursor = conn.cursor()
    cursor.execute('''
                    SELECT movie_id
                    FROM movie
                    WHERE title LIKE ?
                   ''', (f"%{title}%",))
    input_ids = [row[0] for row in cursor.fetchall()]
    conn.close()

    score = validate(input_ids, movie_ids, similarity_matrix)
    print(f"Precision@5 Validation for '{title}': {score:.2f}")

# If the saved matrices exist use them instead of reloading to improve performance 
if os.path.exists("similarity_matrix.npy") and os.path.exists("movie_ids.npy"):
    print("Loading similarity matrix...")

    similarity_matrix = np.load("similarity_matrix.npy")
    movie_ids = np.load("movie_ids.npy")

else:
    print("Building similarity matrix... Please be patient.")

    # Build and combine the feature matrices 
    keyword_matrix, genre_matrix, collection_matrix, company_matrix, movie_ids = create_matrices()
    combined_matrix = combine_matrices(keyword_matrix, genre_matrix, collection_matrix, company_matrix)

    # Create a similarity matrix 
    similarity_matrix = cosine_similarity(combined_matrix)

    # Save computed matrix to improve performance 
    np.save("similarity_matrix.npy", similarity_matrix)
    np.save("movie_ids.npy", movie_ids)

# Map movie IDs to row index in similarity matrix 
id_to_idx = {movie_id: i for i, movie_id in enumerate(movie_ids)}

search_title("starwars")
search_title("indianajones")
search_title("harrypotter")
search_title("avengers")
search_title("lordoftherings")
search_title("thehangover")
search_title("toystory")
