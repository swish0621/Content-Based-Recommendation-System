import sqlite3
from backend.data_processing.preprocess_data import movies, keywords
from backend.db.db_setup import create_database
from backend.db.db_load import load_keywords, load_movies
import os


def run_db_pipeline():
    if not os.path.exists("movies.db"):
        create_database()
        conn = sqlite3.connect("movies.db")
        load_movies(conn, movies)
        load_keywords(conn, keywords)
        conn.close()
        print("Database setup / load complete")

if __name__ == "__main__":
    run_db_pipeline()
