from flask import Flask, render_template, request, redirect, session
from flask_session import Session
from functools import wraps
from tempfile import mkdtemp
import sqlite3
app = Flask(__name__)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("username") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

@app.route("/login/<msg>", methods=["GET", "POST"])
def login(msg):
    """Log user in"""
    
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        session.clear()

        username = request.form.get("username")
        password = request.form.get("password")
        session["username"] = username
        session["password"] = password
        sql1 = f"SELECT *  FROM userInfo WHERE username = '{username}'"
        cursor.execute(sql1)
        data = cursor.fetchone()
        print(data[1], password)
        if data and data[1] == password:
            return redirect("/")
        else:
            return redirect(f"/login/{msg}")
    else:
        return render_template("login.html", data=msg)


# @app.route("/login", methods=["GET", "POST"])
# def login():
#     """Log user in"""

#     # User reached route via POST (as by submitting a form via POST)
#     if request.method == "POST":
#         session.clear()

#         username = request.form.get("username")
#         password = request.form.get("password")
        
#         print(username, password)
#         session["username"] = username
#         session["password"] = password

#         # Redirect user to home page
#         return redirect("/")

#     # User reached route via GET (as by clicking a link or via redirect)
#     else:
#         return render_template("login.html")

# @app.route("/login")
# def user():
#     return request.url

@app.route("/")
@login_required
def index():
   
    return render_template('index.html', user=session["username"], password=session["password"])

@app.route("/upload-file", methods=["POST", "GET"])
def uploader():
    if request.method == 'POST':
        f = request.files['file']
        f.save(f.filename)
        return f.filename


@app.route("/upload")
@login_required
def upload():
    return render_template('upload.html')

