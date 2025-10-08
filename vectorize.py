import sqlite3
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer


def create_matrices():
    # query db for all keywords and their ids 
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


    # create new CountVectorizer obj and create the vectorized keyword matrix 
    keyword_vectorizer = CountVectorizer()
    keyword_matrix = keyword_vectorizer.fit_transform(keywords["keyword_list"])

    # create new CountVectorizer obj and create the vectorized genre matrix 
    genre_vectorizer = CountVectorizer()
    genre_matrix = genre_vectorizer.fit_transform(genres["genre_list"])

    # create new CountVectorizer obj and create the vectorized collection matrix 
    collection_vectorizer = CountVectorizer()
    collection_matrix = collection_vectorizer.fit_transform(collections["collection_list"])

    # create new CountVectorizer obj and create the vectorized collection matrix 
    company_vectorizer = CountVectorizer()
    company_matrix = company_vectorizer.fit_transform(companies["company_list"])



'''
k_matrix = pd.DataFrame(
    keyword_matrix.toarray(),
    columns=keyword_vectorizer.get_feature_names_out()
)
print(k_matrix.head())

g_matrix = pd.DataFrame(
    genre_matrix.toarray(),
    columns=genre_vectorizer.get_feature_names_out()
)
print(g_matrix.head())

c_matrix = pd.DataFrame(
    collection_matrix.toarray(),
    columns=collection_vectorizer.get_feature_names_out()
)
print(c_matrix.head())

company_matrix = pd.DataFrame(
    company_matrix.toarray(),
    columns=company_vectorizer.get_feature_names_out()
)
print(company_matrix.head())
'''



