import sqlite3
from db.db_crud import *


# load movies and their data into the database 
def load_movies(movies):
    for _, row in movies.iterrows():

        # add movie
        movie_id = add_movie(row["title"], row["original_language"], row["popularity"], row["original_id"])

        # insert genres and link
        for genre_name in row["genres"]:
            genre = get_genre_by_name(genre_name)
            if not genre:
                genre_id = add_genre(genre_name)
            else:
                genre_id = genre[0]
            link_movie_to_genre(movie_id, genre_id)

        # insert companies and link 
        for company_name in row["production_companies"]:
            company = get_company_by_name(company_name)
            if not company:
                company_id = add_production_company(company_name)
            else:
                company_id = company[0]
            link_movie_to_company(movie_id, company_id)

        # insert collections and link 
        for collection_name in row["belongs_to_collection"]:
            collection = get_collection_by_name(collection_name)
            if not collection:
                collection_id = add_collection(collection_name)
            else:
                collection_id = collection[0]
            link_movie_to_collection(movie_id, collection_id)

    conn.commit()

def load_keywords(keywords):
    for _, row in keywords.iterrows():
        # get the db id to match many to many table correctly 
        movie_id = get_movie_id_by_original_id(row["id"])
        if movie_id is None:
            continue
        movie_id = movie_id[0]
        # insert keywords and link 
        for keyword_name in row["keyword_lists"]:
            keyword = get_keyword_by_name(keyword_name)
            if not keyword:
                keyword_id = add_keyword(keyword_name)
            else: 
                keyword_id = keyword[0]
            link_movie_to_keyword(movie_id, keyword_id)
    conn.commit()


