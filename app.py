import sqlite3
import os
from flask import Flask, render_template, request, redirect, session, url_for

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "alnoor_secret_key_2026")

DB_PATH = "users.db"

# ---------------- DATABASE ----------------
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price TEXT NOT NULL,
            image TEXT
        )
    """)

    conn.commit()
    conn.close()

init_db()

# ---------------- HOME ----------------
@app.route("/", methods=["GET"])
def home():
    return redirect(url_for("login"))

# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "admin":
            session["user"] = username
            return redirect(url_for("admin"))
        else:
            error = "Invalid username or password"

    return render_template("login.html", error=error)

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

# ---------------- ADMIN ----------------
@app.route("/admin", methods=["GET", "POST"])
def admin():
    if "user" not in session:
        return redirect(url_for("login"))

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    if request.method == "POST":
        name = request.form.get("name")
        price = request.form.get("price")
        image = request.form.get("image", "")

        if name and price:
            cur.execute("INSERT INTO products (name, price, image) VALUES (?, ?, ?)", (name, price, image))
            conn.commit()

    cur.execute("SELECT * FROM products")
    products = cur.fetchall()
    conn.close()

    return render_template("admin.html", products=products)

# ---------------- DELETE PRODUCT ----------------
@app.route("/delete/<int:id>")
def delete(id):
    if "user" not in session:
        return redirect(url_for("login"))

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM products WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return redirect(url_for("admin"))

# ---------------- STORE ----------------
@app.route("/store")
def store():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM products")
    products = cur.fetchall()
    conn.close()

    return render_template("index.html", products=products)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
