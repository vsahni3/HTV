from calendar import leapdays
from re import L
import sqlite3

conn = sqlite3.connect('mydatabase.db')
mycursor = conn.cursor()


def update_user(user_id: int, species_name: str, pic_url: str):
    # create a table for this user if it doesn't already exist
    # user_id -> pic_id
    sql1 = f"CREATE TABLE IF NOT EXISTS user{str(user_id)} (pic_id INTEGER PRIMARY KEY AUTOINCREMENT, species_name nvarchar(100), pic_url nvarchar(200))"
    mycursor.execute(sql1)

    # inserts the user_id, species_name, pic_url
    sql2 = f"INSERT INTO user{str(user_id)} (species_name, pic_url) VALUES ('{species_name}', '{pic_url}')"
    mycursor.execute(sql2)
    conn.commit()


# set up the leaderboard table
sql = '''CREATE TABLE IF NOT EXISTS leaderBoard(
   user_id INTEGER PRIMARY KEY,
   score INTEGER
)'''
mycursor.execute(sql)
conn.commit()
print(mycursor.fetchall())


# updates user information on the leader board
def update_leaderBoard(user_id: int, score: int):
    sql1 = f"SELECT *  FROM leaderBoard WHERE user_id = {user_id}"
    mycursor.execute(sql1)
    # if this user is uploading the photo for the FIRST TIME
    data = mycursor.fetchone()

    if data == None:
        sql2 = f'''
                INSERT INTO leaderBoard (user_id, score)
                VALUES
                ({user_id}, {score})
                '''
        mycursor.execute(sql2)

    else:  # the user uploaded a correct photo before (already in the table)
        add_score = data[1] + score
        sql3 = f'''
                UPDATE leaderBoard
                SET score = {add_score}
                WHERE user_id = {user_id}
                '''
        mycursor.execute(sql3)
    conn.commit()


# def top_ten_leaderboard():
    


update_leaderBoard(60, 20)
sql = f"SELECT *  FROM leaderBoard WHERE user_id = 60"
mycursor.execute(sql)

conn.commit()
