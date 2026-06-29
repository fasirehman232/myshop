import sqlite3

DB_PATH = "users.db"

def update_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    try:
        cur.execute("ALTER TABLE products ADD COLUMN category TEXT DEFAULT 'other'")
        print("Category column added successfully!")
    except sqlite3.OperationalError:
        print("Category column already exists!")
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    update_db()
