import sqlite3
import os

DB_PATH = "users.db"

# Delete old database if exists
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)
    print("Old database deleted!")

# Create new database with all columns
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.execute("""
    CREATE TABLE products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price TEXT NOT NULL,
        image TEXT
    )
""")

conn.commit()
conn.close()
print("New database created with image column!")
