import sqlite3

file = "movies.db"
conn = sqlite3.connect(file)
cursor = conn.cursor()

###############
# MOVIE TABLE #
###############

def add_movie(title, language, popularity):
    cursor.execute(
        "INSERT INTO movie (title, original_language, popularity) VALUES (?, ?, ?)",
        (title, language, popularity)
    )
    movie_id = cursor.lastrowid
    return movie_id

def get_movie(id):
    cursor.execute("SELECT * FROM movie WHERE id = ?", (id,))
    return cursor.fetchone()

def delete_movie(id):
    cursor.execute("DELETE FROM movie WHERE id = ?", (id,))
###############
# GENRE TABLE #
###############

def add_genre(name):
    cursor.execute("INSERT INTO genre (name) VALUES (?)", (name,))
    genre_id = cursor.lastrowid
    return genre_id

def get_genre_by_id(id):
    cursor.execute("SELECT * FROM genre WHERE id = ?", (id,))
    return cursor.fetchone()

def get_genre_by_name(name):
    cursor.execute("SELECT * FROM genre WHERE name = ?", (name,))
    return cursor.fetchone()

def delete_genre(id):
    cursor.execute("DELETE FROM genre WHERE id = ?", (id,))

##################
# MOVIE_TO_GENRE #
##################

def link_movie_to_genre(movie_id, genre_id):
    cursor.execute("INSERT OR IGNORE INTO movie_to_genre (movie_id, genre_id) VALUES(?, ?)", (movie_id, genre_id))
    
######################
# PRODUCTION_COMPANY #
######################

def add_production_company(name):
    cursor.execute("INSERT INTO production_company (name) VALUES (?)", (name,))
    company_id = cursor.lastrowid
    return company_id

def get_company_by_id(id):
    cursor.execute("SELECT * FROM production_company WHERE id = ?", (id,))
    return cursor.fetchone()

def get_company_by_name(name):
    cursor.execute("SELECT * FROM production_company WHERE name = ?", (name,))
    return cursor.fetchone()

def delete_production_company(id):
    cursor.execute("DELETE FROM production_company WHERE id = ?", (id,))

####################
# MOVIE_TO_COMPANY #
####################

def link_movie_to_company(movie_id, company_id):
    cursor.execute("INSERT OR IGNORE INTO movie_to_company (movie_id, company_id) VALUES(?, ?)", (movie_id, company_id))

##############
# COLLECTION #
##############

def add_collection(name):
    cursor.execute("INSERT INTO collection (name) VALUES (?)", (name,))
    collection_id = cursor.lastrowid
    return collection_id

def get_collection_by_id(id):
    cursor.execute("SELECT * FROM collection WHERE id = ?", (id,))
    return cursor.fetchone()

def get_collection_by_name(name):
    cursor.execute("SELECT * FROM collection WHERE name = ?", (name,))
    return cursor.fetchone()

def delete_collection(id):
    cursor.execute("DELETE FROM collection WHERE id = ?", (id,))

#######################
# MOVIE_TO_COLLECTION #
#######################

def link_movie_to_collection(movie_id, collection_id):
    cursor.execute("INSERT OR IGNORE INTO movie_to_collection (movie_id, collection_id) VALUES(?, ?)", (movie_id, collection_id))

###########
# KEYWORD #
###########

def add_keyword(name):
    cursor.execute("INSERT INTO keyword (name) VALUES (?)", (name,))
    keyword_id = cursor.lastrowid
    return keyword_id

def get_keyword_by_id(id):
    cursor.execute("SELECT * FROM keyword WHERE id = ?", (id,))
    return cursor.fetchone()

def get_keyword_by_name(name):
    cursor.execute("SELECT * FROM keyword WHERE name = ?", (name,))
    return cursor.fetchone()

def delete_keyword(id):
    cursor.execute("DELETE FROM keyword WHERE id = ?", (id,))

####################
# MOVIE_TO_KEYWORD #
####################

def link_movie_to_keyword(movie_id, keyword_id):
    cursor.execute("INSERT OR IGNORE INTO movie_to_keyword (movie_id, keyword_id) VALUES(?, ?)", (movie_id, keyword_id))
