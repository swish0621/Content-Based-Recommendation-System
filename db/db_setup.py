import sqlite3

def create_database():
   conn = sqlite3.connect("movies.db")
   cursor = conn.cursor()

   cursor.executescript('''
                  CREATE TABLE IF NOT EXISTS movie (
                  movie_id INTEGER PRIMARY KEY AUTOINCREMENT,                  -- unique movie identifier
                  title TEXT NOT NULL,                                         -- movie title
                  original_language TEXT,                                      -- original language of the movie
                  popularity INTEGER,                                          -- numeric poularity score 
                  original_id INTEGER NOT NULL                                 -- original id from dataset
                  );

                  CREATE TABLE IF NOT EXISTS genre (
                  genre_id INTEGER PRIMARY KEY AUTOINCREMENT,                  -- unique genre identifier
                  name TEXT UNIQUE NOT NULL                                    -- unique genre name 
                  );

                  CREATE TABLE IF NOT EXISTS movie_to_genre (
                  movie_id INTEGER NOT NULL,                                   -- foreign key to movie
                  genre_id INTEGER NOT NULL,                                   -- foreign key to genre
                  PRIMARY KEY (movie_id, genre_id),                            -- composite primary key
                  FOREIGN KEY (movie_id) REFERENCES movie(movie_id),
                  FOREIGN KEY (genre_id) REFERENCES genre(genre_id)
                  );

                  CREATE TABLE IF NOT EXISTS production_company (
                  company_id INTEGER PRIMARY KEY AUTOINCREMENT,                -- unique production_company identifier
                  name TEXT UNIQUE NOT NULL                                    -- required unique company name
                  );

                  CREATE TABLE IF NOT EXISTS movie_to_company (
                  movie_id INTEGER NOT NULL,                                   -- foreign key to movie
                  company_id INTEGER NOT NULL,                                 -- foreign key to production_company
                  PRIMARY KEY (movie_id, company_id),                          -- composite primary key
                  FOREIGN KEY (movie_id) REFERENCES movie(movie_id),
                  FOREIGN KEY (company_id) REFERENCES production_company(company_id)
                  );

                  CREATE TABLE IF NOT EXISTS collection (
                  collection_id INTEGER PRIMARY KEY AUTOINCREMENT,             -- unique collection id
                  name TEXT UNIQUE NOT NULL                                    -- unique collection name
                  );

                  CREATE TABLE IF NOT EXISTS movie_to_collection (
                  movie_id INTEGER NOT NULL,                                   -- foreign key to movie
                  collection_id INTEGER NOT NULL,                              -- foreign key to collection 
                  PRIMARY KEY (movie_id, collection_id),
                  FOREIGN KEY (movie_id) REFERENCES movie(movie_id),
                  FOREIGN KEY (collection_id) REFERENCES collection(collection_id)
                  );

                  CREATE TABLE IF NOT EXISTS keyword (
                  keyword_id INTEGER PRIMARY KEY AUTOINCREMENT,                -- unique keyword identifier
                  name TEXT UNIQUE NOT NULL                                    -- unique keyword name
                  );

                  CREATE TABLE IF NOT EXISTS movie_to_keyword (
                  movie_id INTEGER NOT NULL,                                   -- foreign key to movie
                  keyword_id INTEGER NOT NULL,                                 -- foreign key to keyword
                  PRIMARY KEY (movie_id, keyword_id),
                  FOREIGN KEY (movie_id) REFERENCES movie(movie_id),
                  FOREIGN KEY (keyword_id) REFERENCES keyword(keyword_id)
                  );

               ''')
   cursor.execute("CREATE INDEX IF NOT EXISTS idx_movie_original_id ON movie(original_id);")
   conn.commit()
   conn.close()

