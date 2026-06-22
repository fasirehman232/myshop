import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "alnoor_secret_key_2026_advance")
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"
UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'images')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ---------------- DATABASE INIT ----------------

def init_db():
    conn = sqlite3.connect("users.db")
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

    # Add admin user if not exists
    cur.execute("SELECT * FROM users WHERE username = ?", (ADMIN_USERNAME,))
    if not cur.fetchone():
        cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (ADMIN_USERNAME, ADMIN_PASSWORD))

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

        conn = sqlite3.connect("users.db")
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

        conn = sqlite3.connect("users.db")
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

    conn = sqlite3.connect("users.db")
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
    if session["user"] != ADMIN_USERNAME:
        return redirect(url_for("store"))  # Non-admins go back to store

    conn = sqlite3.connect("users.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM products")
    products = cur.fetchall()

    conn.close()

    return render_template("admin.html", products=products)


# ---------------- ADD PRODUCT ----------------

@app.route("/add", methods=["POST"])
def add():
    if "user" not in session or session["user"] != ADMIN_USERNAME:
        return redirect(url_for("login"))
        
    name = request.form["name"]
    price = request.form["price"]
    
    # Check if file is uploaded
    if 'image' not in request.files:
        return "No file part", 400
    file = request.files['image']
    if file.filename == '':
        return "No selected file", 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        image_path = f"images/{filename}"
    
        conn = sqlite3.connect("users.db")
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO products (name, price, image) VALUES (?, ?, ?)",
            (name, price, image_path)
        )

        conn.commit()
        conn.close()

    return redirect(url_for("admin"))


# ---------------- DELETE PRODUCT ----------------

@app.route("/delete/<int:id>")
def delete(id):
    if "user" not in session or session["user"] != ADMIN_USERNAME:
        return redirect(url_for("login"))
        
    conn = sqlite3.connect("users.db")
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