import sqlite3

DB_PATH = "users.db"

def add_banners_table():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS banners (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            text TEXT,
            background TEXT
        )
    """)
    
    # Insert default banners if none exist
    cur.execute("SELECT COUNT(*) FROM banners")
    if cur.fetchone()[0] == 0:
        default_banners = [
            ("🎉 Special Discount!", "Get 20% off on all Vegetables!", "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"),
            ("🥤 Fresh Juices!", "Buy 2 Get 1 Free!", "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)"),
            ("📱 New Mobiles!", "Limited Stock Available!", "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)"),
        ]
        cur.executemany("INSERT INTO banners (title, text, background) VALUES (?, ?, ?)", default_banners)
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    add_banners_table()
