from flask import Flask, render_template, request, redirect, session
from flask_session import Session
from functools import wraps
from os import remove
from tempfile import mkdtemp
from datetime import datetime
from score_functions import dexter
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
            return redirect("/login/good")
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
            return redirect(f"/login/Invalid Login")
    else:
        return render_template("login.html", data=msg)


# @app.route("/login", methods=["GET", "POST"])
# def login():
#     """Log user in"""
#     conn = sqlite3.connect('mydatabase.db')
#     cursor = conn.cursor()


#     # User reached route via POST (as by submitting a form via POST)
#     if request.method == "POST":
#         session.clear()

#         username = request.form.get("username")
#         password = request.form.get("password")

#         print(username, password)
#         session["username"] = username
#         session["password"] = password

#         sql1 = f"SELECT *  FROM userInfo WHERE username = '{username}'"
#         cursor.execute(sql1)
#         data = cursor.fetchone()
#         print(data[1], password)
#         if data and data[1] == password:
#             print(10)
#             return redirect("/")
#         else:
#             print(5)
#             return redirect("/login/Invalid Login")
#     else:
#         print(15)
#         return render_template("login.html", data=msg)


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


    #     # Redirect user to home page
    #     return redirect("/")

    # # User reached route via GET (as by clicking a link or via redirect)
    # else:
    #     return render_template("login.html")


# @app.route("/login")
# def user():
#     return request.url


@app.route("/challenges")
@login_required
def challenges():
    current_challenge = {
        'start_date': datetime(2022, 10, 9, 0, 0, 0),
        'species_name': {
            # palm tree
            'Cocos nucifera': 3000,
            # neem tree
            'Azadirachta indica': 2000,
            'cucumber': 1000
        }
    }
    session['current_challenge'] = current_challenge
    with open("app/templates/contest_prize_pool.txt", "r") as f:
        pool = int(f.readline())
    return render_template('challenges.html', pool=pool)


@app.route("/donate", methods=['GET', 'POST'])
@login_required
def donate():
    if request.method == 'POST':
        donation_amount = int(request.form.get("donate"))
        username = session["username"]
        if "TODO: user has enough money: user table, parameters(username, donation_amount) -> bool":
            "TODO: remove money from user: user table, parameters(username, donation_amount) -> None"
            with open("app/templates/contest_prize_pool.txt", "r") as f:
                pool = int(f.readline())
            # update new pool
            with open("app/templates/contest_prize_pool.txt", "w") as f:
                f.write(str(pool + donation_amount))

        return redirect("/challenges")
    else:
        return render_template('donate.html')


@app.route("/")
@login_required
def index():
    return render_template('index.html', user=session["username"], password=session["password"])


@app.route("/upload-file", methods=["POST", "GET"])
def uploader():
    if request.method == 'POST':
        f = request.files['file']
        f.save(f.filename)
        username = session["username"]
        current_challenge = session["current_challenge"]
        found_score = dexter(f.filename, current_challenge["species_name"], current_challenge["start_date"])

        conn = sqlite3.connect('mydatabase.db')
        cursor = conn.cursor()
        sql1 = f"SELECT user_id FROM userInfo WHERE username = '{username}'"
        cursor.execute(sql1)
        user_id = cursor.fetchone()
        print(user_id)

        "TODO: add found score to user score in leaderboard: leaderboard, parameters(user_id, found_score) -> None"
        remove(f.filename)
        "TODO: display the score result on challenges page? not SQL so get varun to do it"
        return redirect("/challenges")


@app.route("/upload")
@login_required
def upload():
    return render_template('upload.html')
