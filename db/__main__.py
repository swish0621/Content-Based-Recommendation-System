import sqlite3
from preprocess_data import movies, keywords
from db.db_setup import create_database
from db.db_load import load_keywords, load_movies



create_database()
load_keywords(keywords)
load_movies(movies)
print("Database setup / load complete")
