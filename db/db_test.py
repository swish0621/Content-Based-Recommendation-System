import sqlite3
conn = sqlite3.connect("movies.db")
cursor = conn.cursor()
cursor.execute("SELECT * FROM movie")
print(cursor.fetchmany(10))
cursor.execute("SELECT COUNT(id) FROM keyword")
print(cursor.fetchmany(10))

