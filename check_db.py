
import sqlite3

conn = sqlite3.connect("users.db")
cur = conn.cursor()

cur.execute("SELECT * FROM products")
products = cur.fetchall()
print("Products in database:")
for p in products:
    print(f"ID: {p[0]}, Name: {p[1]}, Price: {p[2]}, Image: {p[3]}")

conn.close()

