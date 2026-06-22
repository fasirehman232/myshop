
import sqlite3
import os

# Delete old database
if os.path.exists("users.db"):
    os.remove("users.db")
    print("Old database deleted!")

# Initialize fresh database
print("Creating fresh database...")

# Now just initialize fresh with app.py
from app import init_db
init_db()

print("Database reset complete! Now you can add your own products!")
