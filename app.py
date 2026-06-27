import sqlite3
import os
from flask import Flask, render_template, request, redirect, session, url_for
import re
from werkzeug.utils import secure_filename
from uuid import uuid4

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "alnoor_secret_key_2026")

app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create uploads folder if not exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def is_local_image(path):
    """Check if the path is a local file or a remote URL"""
    if not path:
        return False
    # Check if it starts with http:// or https://
    if re.match(r'^https?://', path):
        return False
    return True

app.jinja_env.filters['is_local'] = is_local_image

DB_PATH = "users.db"

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

init_db()


# ---------------- GOOGLE VERIFY (ADD THIS) ----------------
@app.route('/google123456789abcdef.html')
def google_verify():
    return app.send_static_file('google123456789abcdef.html')


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
        image_url = request.form.get("image", "")
        image_file = request.files.get("image_file")

        image = image_url

        # file upload
        if image_file and allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            unique_filename = f"{uuid4().hex}_{filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            image_file.save(filepath)
            image = f"/static/uploads/{unique_filename}"

        if name and price:
            cur.execute(
                "INSERT INTO products (name, price, image) VALUES (?, ?, ?)",
                (name, price, image)
            )
            conn.commit()

    cur.execute("SELECT * FROM products")
    products = cur.fetchall()
    conn.close()

    return render_template("admin.html", products=products)


# ---------------- EDIT ----------------
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    if "user" not in session:
        return redirect(url_for("login"))

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    if request.method == "POST":
        name = request.form.get("name")
        price = request.form.get("price")
        image_url = request.form.get("image", "")
        image_file = request.files.get("image_file")

        image = image_url

        if image_file and allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            unique_filename = f"{uuid4().hex}_{filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            image_file.save(filepath)
            image = f"/static/uploads/{unique_filename}"

        if name and price:
            if image:
                cur.execute(
                    "UPDATE products SET name=?, price=?, image=? WHERE id=?",
                    (name, price, image, id)
                )
            else:
                cur.execute(
                    "UPDATE products SET name=?, price=? WHERE id=?",
                    (name, price, id)
                )

            conn.commit()
            conn.close()
            return redirect(url_for("admin"))

    cur.execute("SELECT * FROM products WHERE id=?", (id,))
    product = cur.fetchone()
    conn.close()

    if not product:
        return redirect(url_for("admin"))

    return render_template("edit.html", product=product)


# ---------------- DELETE ----------------
@app.route("/delete/<int:id>")
def delete(id):
    if "user" not in session:
        return redirect(url_for("login"))

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM products WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect(url_for("admin"))


# ---------------- CLIENT SIGNUP ----------------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    error = None
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        
        try:
            cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            conn.close()
            session["client_user"] = username
            return redirect(url_for("store"))
        except sqlite3.IntegrityError:
            error = "Username already exists!"
            conn.close()
    
    return render_template("signup.html", error=error)


# ---------------- CLIENT LOGIN ----------------
@app.route("/client-login", methods=["GET", "POST"])
def client_login():
    error = None
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cur.fetchone()
        conn.close()
        
        if user:
            session["client_user"] = username
            return redirect(url_for("store"))
        else:
            error = "Invalid username or password!"
    
    return render_template("client_login.html", error=error)


# ---------------- CLIENT LOGOUT ----------------
@app.route("/client-logout")
def client_logout():
    session.pop("client_user", None)
    return redirect(url_for("store"))


# ---------------- STORE ----------------
@app.route("/store")
def store():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM products")
    products = cur.fetchall()
    conn.close()

    return render_template("index.html", products=products, client_user=session.get("client_user"))


# ---------------- RUN ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)