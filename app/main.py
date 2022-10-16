from flask import Flask, render_template, request, redirect, session
from flask_session import Session
from functools import wraps
from os import remove
from tempfile import mkdtemp
from datetime import datetime
from dummy_table_function import add_found_score, calc_user_progress, enough_money, remove_money
from score_functions import dexter
import sqlite3
from location import give_region

app = Flask(__name__)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

current_challenge = {
    'start_date': datetime(2022, 10, 9, 0, 0, 0),
    'species_name': {
        # palm tree
        'Cocos nucifera': 3000,
        # neem tree
        'Azadirachta indica': 2000,
        'Dionaea muscipula': 1000
    }
    }

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
        sql1 = f"SELECT * FROM userInfo WHERE username = '{username}'"
        cursor.execute(sql1)
        data = cursor.fetchone()
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


@app.route("/challenges/<optional>")
@login_required
def challenges(optional):
    region = give_region()

    with open("app/templates/contest_prize_pool.txt", "r") as f:
        pool = int(f.readline())
    data = [region, pool, list(current_challenge["species_name"].keys()), list(current_challenge["species_name"].values())]
    if optional != 'null':
        data.append(int(optional))
    return render_template('challenges.html', data=data)


@app.route("/donate", methods=['GET', 'POST'])
@login_required
def donate():
    if request.method == 'POST':
        donation_amount = int(request.form.get("donate"))
        username = session["username"]
        if enough_money(username, donation_amount):
            remove_money(username, donation_amount)
            with open("app/templates/contest_prize_pool.txt", "r") as f:
                pool = int(f.readline())
            # update new pool
            with open("app/templates/contest_prize_pool.txt", "w") as f:
                f.write(str(pool + donation_amount))

        return redirect("/challenges/null")
    else:
        return render_template('donate.html')


@app.route("/")
@login_required
def index():

    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    cursor.execute(f"""SELECT user_id, money FROM userInfo WHERE username = '{session["username"]}'""")
    user_id, money = cursor.fetchone()
    cursor.execute(f'SELECT species_name, pic_url FROM user{user_id}')
    data = cursor.fetchall()
    cursor.execute(f"""SELECT score FROM leaderBoard WHERE user_id = '{user_id}'""")
    score = cursor.fetchone()[0]
    species_seen = calc_user_progress(user_id, list(current_challenge["species_name"].keys()))
    data = [score, money, data, list(current_challenge["species_name"].keys()), species_seen]
    return render_template('index.html', user=session["username"], password=session["password"], data=data)


@app.route("/upload-file", methods=["POST", "GET"])
def uploader():
    if request.method == 'POST':
        conn = sqlite3.connect('mydatabase.db')
        cursor = conn.cursor()
        f = request.files['file']
        f.save(f.filename)
        username = session["username"]
        sql1 = f"SELECT user_id FROM userInfo WHERE username = '{username}'"
        cursor.execute(sql1)
        user_id = cursor.fetchone()[0]
        found_score = dexter(user_id, f.filename, current_challenge["species_name"], current_challenge["start_date"])

        add_found_score(user_id, found_score)
        remove(f.filename)
        
        return redirect("/challenges/" + str(found_score))


@app.route("/upload")
@login_required
def upload():
    return render_template('upload.html')

@app.route("/leaderboard")
@login_required
def leaderboard():
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    sql1 = "SELECT username FROM userInfo WHERE user_id in (SELECT user_id FROM leaderBoard)"
    cursor.execute(sql1)
    usernames = cursor.fetchall()
    print(usernames)

    cursor.execute("SELECT score FROM leaderBoard")
    scores = cursor.fetchall()
    print(scores)
    counts = range(1, 6)
    data = sorted([[scores[i][0], usernames[i][0].title()] for i in range(5)], key=lambda x: x[0], reverse=True)
    data = [[data[i][0], counts[i], data[i][1]] for i in range(5)]
    return render_template('leaderboards.html', data=data)
    




