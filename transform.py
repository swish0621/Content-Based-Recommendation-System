import sqlite3
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.preprocessing import OneHotEncoder
from scipy.sparse import hstack

# will return 4 seperate unweighted matrices in the order of keyword_matrix, genre_matrix, collection_matrix, company_matrix and the movie ids
# the matrix values are collected directly from querying the sql db 
def create_matrices():

    conn = sqlite3.connect("movies.db")
    cursor = conn.cursor()

    # create keywords dataframe with movie_id and a space separated list of keywords 
    keywords = pd.read_sql_query('''
                                SELECT m.movie_id, GROUP_CONCAT(k.name, \" \") as keyword_list 
                                FROM movie_to_keyword m 
                                JOIN keyword k 
                                ON m.keyword_id = k.keyword_id 
                                GROUP BY m.movie_id 
                                ORDER BY m.movie_id;
                                ''', conn)

    # create genres dataframe with movie_id and a space separated list of genres
    genres = pd.read_sql_query('''
                                SELECT m.movie_id, GROUP_CONCAT(g.name, \" \") as genre_list
                                FROM movie_to_genre m
                                JOIN genre g
                                ON m.genre_id = g.genre_id
                                GROUP BY m.movie_id
                                ORDER BY m.movie_id;
                                ''', conn)

    # create collections dataframe with movie_id and a space separated list of collections
    collections = pd.read_sql_query('''
                                SELECT m.movie_id, GROUP_CONCAT(c.name, \" \") as collection_list
                                FROM movie_to_collection m
                                JOIN collection c
                                ON m.collection_id = c.collection_id
                                GROUP BY m.movie_id
                                ORDER BY m.movie_id;
                                ''', conn)

    # create companies dataframe with movie_id and a space separated list of companies
    companies = pd.read_sql_query('''
                                SELECT m.movie_id, GROUP_CONCAT(c.name, \" \") as company_list
                                FROM movie_to_company m
                                JOIN production_company c
                                ON m.company_id = c.company_id
                                GROUP BY m.movie_id
                                ORDER BY m.movie_id;
                                ''', conn)
    movie_ids = pd.read_sql_query(''' 
                                SELECT movie_id FROM movie ORDER BY movie_id
                               ''', conn)
    conn.close()

    movie_ids = movie_ids["movie_id"].values
    keywords = keywords.set_index("movie_id").reindex(movie_ids, fill_value="")
    genres = genres.set_index("movie_id").reindex(movie_ids, fill_value="")
    collections = collections.set_index("movie_id").reindex(movie_ids, fill_value="")
    companies = companies.set_index("movie_id").reindex(movie_ids, fill_value="")

    genres["genre_list"] = genres["genre_list"].apply(lambda x: x.split() if isinstance(x,str) and x else[])
    companies["company_list"] = companies["company_list"].apply(lambda x: x.split() if isinstance(x,str) and x else[])
    
    # create new TfidfVectorizer obj and create the vectorized keyword matrix 
    # downweights the most common terms and upweights rarer keywords 
    keyword_vectorizer = TfidfVectorizer()
    keyword_matrix = keyword_vectorizer.fit_transform(keywords["keyword_list"])

    # create new MultiLabelBinarizer obj and create the genre matrix 
    genre_encoder = MultiLabelBinarizer()
    genre_matrix = genre_encoder.fit_transform(genres["genre_list"])

    # create new OneHotEncoder obj and create the collection matrix 
    collection_encoder = OneHotEncoder()
    collection_matrix = collection_encoder.fit_transform(collections["collection_list"].values.reshape(-1, 1))

    # create new MultiLabelBinarizer obj and create the company matrix 
    company_encoder = MultiLabelBinarizer()
    company_matrix = company_encoder.fit_transform(companies["company_list"])

    return keyword_matrix, genre_matrix, collection_matrix, company_matrix, movie_ids



# input 4 seperate matrices and optionally weights in list form [keyword_weight, genre_weight, collection_weight, company_weight]
# they will be weighted / combined using hstack
# returns 1 matrix
def combine_matrices(keyword_matrix, genre_matrix, collection_matrix, company_matrix, weights=None):
    if weights:
        keyword_matrix *= weights[0]
        genre_matrix *= weights[1]
        collection_matrix *= weights[2]
        company_matrix *= weights[3]
    combined = hstack([keyword_matrix, genre_matrix, collection_matrix, company_matrix])
    return combined



