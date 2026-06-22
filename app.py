import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session
import os
import sys

# Get correct path for templates and static files
def get_resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, relative_path)


# Get correct path for database
def get_db_path():
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, "users.db")


app = Flask(
    __name__,
    template_folder=get_resource_path("templates"),
    static_folder=get_resource_path("static")
)

app.secret_key = "alnoor_secret_key_2026_advance"


# ---------------- DATABASE INIT ----------------

def init_db():
    conn = sqlite3.connect(get_db_path())
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            price TEXT,
            image TEXT
        )
    """)

    cur.execute("SELECT COUNT(*) FROM products")

    if cur.fetchone()[0] == 0:
        initial_products = [
            ("Smart Watch", "799", "images/watch.jpg"),
            ("Hand Free", "499", "images/hand_free.png"),
            ("Mobile Glass", "299", "images/mobile_glass.jpg"),
            ("USB Cable", "499", "images/usb.jpg"),
            ("Fast Charger", "699", "images/fast_charger.jpg")
        ]

        cur.executemany(
            "INSERT INTO products (name, price, image) VALUES (?, ?, ?)",
            initial_products
        )

    conn.commit()
    conn.close()


init_db()


# ---------------- HOME ----------------

@app.route("/")
def home():
    return redirect(url_for("login"))


# ---------------- SIGNUP ----------------

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect(get_db_path())
        cur = conn.cursor()

        try:
            cur.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password)
            )

            conn.commit()
            conn.close()

            return redirect(url_for("login"))

        except sqlite3.IntegrityError:
            conn.close()
            return render_template(
                "signup.html",
                error="User already exists"
            )

    return render_template("signup.html")


# ---------------- LOGIN ----------------

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect(get_db_path())
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        )

        user = cur.fetchone()
        conn.close()

        if user:
            session["user"] = username
            return redirect(url_for("store"))

        return render_template(
            "login.html",
            error="Invalid login"
        )

    return render_template("login.html")


# ---------------- STORE ----------------

@app.route("/store")
def store():
    if "user" not in session:
        return redirect(url_for("login"))

    conn = sqlite3.connect(get_db_path())
    cur = conn.cursor()

    cur.execute("SELECT * FROM products")
    products = cur.fetchall()

    conn.close()

    return render_template("index.html", products=products)


# ---------------- ADMIN ----------------

@app.route("/admin")
def admin():
    if "user" not in session:
        return redirect(url_for("login"))

    conn = sqlite3.connect(get_db_path())
    cur = conn.cursor()

    cur.execute("SELECT * FROM products")
    products = cur.fetchall()

    conn.close()

    return render_template("admin.html", products=products)


# ---------------- ADD PRODUCT ----------------

@app.route("/add", methods=["POST"])
def add():
    name = request.form["name"]
    price = request.form["price"]
    image = request.form["image"]

    conn = sqlite3.connect(get_db_path())
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO products (name, price, image) VALUES (?, ?, ?)",
        (name, price, image)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("admin"))


# ---------------- DELETE PRODUCT ----------------

@app.route("/delete/<int:id>")
def delete(id):
    conn = sqlite3.connect(get_db_path())
    cur = conn.cursor()

    cur.execute("DELETE FROM products WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return redirect(url_for("admin"))


# ---------------- LOGOUT ----------------

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


# ---------------- RUN APP ----------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)