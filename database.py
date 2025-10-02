import sqlite3

conn = sqlite3.connect("movies.db")
cursor = conn.cursor()

cursor.execute('''
               CREATE TABLE IF NOT EXISTS movie (
               id INTEGER PRIMARY KEY AUTO INCREMENT,                       -- unique movie identifier
               title TEXT NOT NULL,                                         -- movie title
               original_language TEXT,                                      -- original language of the movie
               popularity INTEGER                                           -- numeric poularity score 
               );

               CREATE TABLE IF NOT EXISTS genre (
               id INTEGER PRIMARY KEY AUTO INCREMENT,                       -- unique genre identifier
                name TEXT UNIQUE NOT NULL                                   -- unique genre name 
               );

               CREATE TABLE IF NOT EXISTS movie_to_genre (
               movie_id INTEGER NOT NULL,                                   -- foreign key to movie
               genre_id INTEGER NOT NULL,                                   -- foreign key to genre
               PRIMARY KEY (movie_id, genre_id),                            -- composite primary key
               FOREIGN KEY (movie_id) REFERENCES movie(id),
               FOREIGN KEY (genre_id) REFERENCES genre(id)
               );

               CREATE TABLE IF NOT EXISTS production_company (
               id INTEGER PRIMARY KEY AUTO INCREMENT,                       -- unique production_company identifier
               name TEXT UNIQUE NOT NULL                                    -- required unique company name
               );

               CREATE TABLE IF NOT EXISTS movie_to_company (
               movie_id INTEGER NOT NULL,                                   -- foreign key to movie
               company_id INTEGER NOT NULL,                                 -- foreign key to production_company
               PRIMARY KEY (movie_id, company_id),                          -- composite primary key
               FOREIGN KEY (movie_id) REFERENCES movie(id),
               FOREIGN KEY (company_id) REFERENCES (production_company)
               );

               CREATE TABLE IF NOT EXISTS collection (
               id INTEGER PRIMARY KEY AUTO INCREMENT,                       -- unique collection id
               name TEXT UNIQUE NOT NULL                                    -- unique collection name
               );

               CREATE TABLE IF NOT EXISTS movie_to_collection (
               movie_id INTEGER NOT NULL,                                   -- foreign key to movie
               collection_id INTEGER NOT NULL,                              -- foreign key to collection 
               PRIMARY KEY (movie_id, collection_id),
               FOREIGN KEY (movie_id) REFERENCES movie(id),
               FOREIGN KEY (collection id) REFERENCES collection(id)
               );

               CREATE TABLE IF NOT EXISTS keyword (
               id INTEGER PRIMARY KEY AUTO INCREMENT,                       -- unique keyword identifier
               name TEXT UNIQUE NOT NULL                                    -- unique keyword name

               CREATE TABLE IF NOT EXISTS movie_to_keyword (
               movie_id INTEGER NOT NULL,                                   -- foreign key to movie
               keyword_id INTEGER NOT NULL,                                 -- foreign key to keyword
               PRIMARY KEY (movie_id, keyword_id),
               FOREIGN KEY (movie_id) REFERENCES movie(id),
               FOREIGN KEY (keyword_id) REFERENCES keyword(id),
               );

            ''')
conn.commit()
conn.close()

