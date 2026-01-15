# ---------------------------------------------
# Definitions of Table Specific CRUD Operations 
# ---------------------------------------------

import sqlite3


# -----------
# MOVIE TABLE 
# -----------
def add_movie(conn, title, language, popularity, original_id, original_title):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO movie (title, original_language, popularity, original_id, original_title) VALUES (?, ?, ?, ?, ?)",
        (title, language, popularity, original_id, original_title)
    )
    movie_id = cursor.lastrowid
    return movie_id

def get_movie(conn, id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM movie WHERE movie_id = ?", (id,))
    return cursor.fetchone()

def get_movie_id_by_original_id(conn, original_id):
    cursor = conn.cursor()
    cursor.execute("SELECT movie_id FROM movie WHERE original_id = ?", (original_id,))
    return cursor.fetchone()

def delete_movie(conn, id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM movie WHERE movie_id = ?", (id,))

# -----------
# GENRE TABLE 
# -----------
def add_genre(conn, name):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO genre (name) VALUES (?)", (name,))
    genre_id = cursor.lastrowid
    return genre_id

def get_genre_by_id(conn, id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM genre WHERE genre_id = ?", (id,))
    return cursor.fetchone()

def get_genre_by_name(conn, name):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM genre WHERE name = ?", (name,))
    return cursor.fetchone()

def delete_genre(conn, id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM genre WHERE genre_id = ?", (id,))

# --------------
# MOVIE_TO_GENRE 
# --------------
def link_movie_to_genre(conn, movie_id, genre_id):
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO movie_to_genre (movie_id, genre_id) VALUES(?, ?)", (movie_id, genre_id))
    
# ------------------
# PRODUCTION_COMPANY
# ------------------
def add_production_company(conn, name):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO production_company (name) VALUES (?)", (name,))
    company_id = cursor.lastrowid
    return company_id

def get_company_by_id(conn, id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM production_company WHERE company_id = ?", (id,))
    return cursor.fetchone()

def get_company_by_name(conn, name):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM production_company WHERE name = ?", (name,))
    return cursor.fetchone()

def delete_production_company(conn, id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM production_company WHERE company_id = ?", (id,))

# ----------------
# MOVIE_TO_COMPANY 
# ----------------
def link_movie_to_company(conn, movie_id, company_id):
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO movie_to_company (movie_id, company_id) VALUES(?, ?)", (movie_id, company_id))

# ----------
# COLLECTION 
# ----------
def add_collection(conn, name):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO collection (name) VALUES (?)", (name,))
    collection_id = cursor.lastrowid
    return collection_id

def get_collection_by_id(conn, id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM collection WHERE collection_id = ?", (id,))
    return cursor.fetchone()

def get_collection_by_name(conn, name):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM collection WHERE name = ?", (name,))
    return cursor.fetchone()

def delete_collection(conn, id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM collection WHERE collection_id = ?", (id,))

# -------------------
# MOVIE_TO_COLLECTION 
# -------------------
def link_movie_to_collection(conn, movie_id, collection_id):
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO movie_to_collection (movie_id, collection_id) VALUES(?, ?)", (movie_id, collection_id))

# -------
# KEYWORD 
# -------
def add_keyword(conn, name):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO keyword (name) VALUES (?)", (name,))
    keyword_id = cursor.lastrowid
    return keyword_id

def get_keyword_by_id(conn, id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM keyword WHERE keyword_id = ?", (id,))
    return cursor.fetchone()

def get_keyword_by_name(conn, name):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM keyword WHERE name = ?", (name,))
    return cursor.fetchone()

def delete_keyword(conn, id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM keyword WHERE keyword_id = ?", (id,))

# ----------------
# MOVIE_TO_KEYWORD 
# ----------------
def link_movie_to_keyword(conn, movie_id, keyword_id):
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO movie_to_keyword (movie_id, keyword_id) VALUES(?, ?)", (movie_id, keyword_id))
