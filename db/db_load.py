import sqlite3
from db.db_crud import *


# load movies and their data into the database 
def load_movies(conn, movies):
    for _, row in movies.iterrows():

        # add movie
        movie_id = add_movie(conn, row["title"], row["original_language"], row["popularity"], row["original_id"])

        # insert genres and link
        for genre_name in row["genres"]:
            genre = get_genre_by_name(conn, genre_name)
            if not genre:
                genre_id = add_genre(conn, genre_name)
            else:
                genre_id = genre[0]
            link_movie_to_genre(conn, movie_id, genre_id)

        # insert companies and link 
        for company_name in row["production_companies"]:
            company = get_company_by_name(conn, company_name)
            if not company:
                company_id = add_production_company(conn, company_name)
            else:
                company_id = company[0]
            link_movie_to_company(conn, movie_id, company_id)

        # insert collections and link 
        for collection_name in row["belongs_to_collection"]:
            collection = get_collection_by_name(conn, collection_name)
            if not collection:
                collection_id = add_collection(conn, collection_name)
            else:
                collection_id = collection[0]
            link_movie_to_collection(conn, movie_id, collection_id)

    conn.commit()


def load_keywords(conn, keywords):

    for _, row in keywords.iterrows():
        # get the db id to match many to many table correctly 
        movie_id = get_movie_id_by_original_id(conn, row["original_id"])
        if movie_id is None:
            print("skipped keyword")
            continue
        movie_id = movie_id[0]
        # insert keywords and link 
        for keyword_name in row["keyword_lists"]:
            keyword = get_keyword_by_name(conn, keyword_name)
            if not keyword:
                keyword_id = add_keyword(conn, keyword_name)
            else: 
                keyword_id = keyword[0]
            link_movie_to_keyword(conn, movie_id, keyword_id)
    conn.commit()



