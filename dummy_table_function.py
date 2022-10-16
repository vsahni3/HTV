import sqlite3
from turtle import update

conn = sqlite3.connect('mydatabase.db')
mycursor = conn.cursor()
# mycursor.execute('DELETE FROM userInfo WHERE user_id > 5')
# mycursor.execute('SELECT * FROM userInfo')
# print(mycursor.fetchall())
# mycursor.execute('DELETE FROM leaderBoard WHERE user_id > 5')
# mycursor.execute('SELECT * FROM leaderBoard')
# print(mycursor.fetchall())


#initialize the user_info table
sqlU = f"CREATE TABLE IF NOT EXISTS userInfo (user_id INTEGER PRIMARY KEY AUTOINCREMENT, password nvarchar(100), username nvarchar(100), money INTEGER)"
mycursor.execute(sqlU)

sqlU2 = f'''
        INSERT INTO userInfo (password, username, money)
        VALUES
        ('1234', 'sungjin', 1111111), 
        ('2345', 'hong', 111), 
        ('3456', 'varun', 111), 
        ('4567', 'tyseer', 11111), 
        ('5678', 'michael', 1111) 
        '''
# mycursor.execute(sqlU2)
# conn.commit()

# mycursor.execute('SELECT * FROM user3')
# print(mycursor.fetchall())
# sql1 = "CREATE TABLE IF NOT EXISTS user3 (pic_id INTEGER PRIMARY KEY AUTOINCREMENT, species_name nvarchar(100), pic_url nvarchar(200))"
# mycursor.execute(sql1)
# mycursor.execute("INSERT INTO user3 (species_name, pic_url) VALUES ('Aloe vera', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRYXB6Cq5qG0VEUXD8B-ni2j9HHwsep9rZncA&usqp=CAU')")
# mycursor.execute("INSERT INTO user3 (species_name, pic_url) VALUES ('Bambusa vulgaris', 'https://images.squarespace-cdn.com/content/v1/5e5cd082c50ea102c52e5bb0/1590049336762-S27YM4UE2NKLPEECQZE8/Bambusa+vulgaris')")
# mycursor.execute("INSERT INTO user3 (species_name, pic_url) VALUES ('Elaeagnus angustifolia', 'https://www.nature-and-garden.com/wp-content/uploads/sites/4/2018/06/russian-olive-invasive-tree.jpg')")
# mycursor.execute("INSERT INTO user3 (species_name, pic_url) VALUES ('Rhamnus cathartica', 'https://newfs.s3.amazonaws.com/taxon-images-1000s1000/Rhamnaceae/rhamnus-cathartica-fr-ahaines.jpg')")
# mycursor.execute("INSERT INTO user3 (species_name, pic_url) VALUES ('Cornus canadensis', 'https://www.gardenia.net/storage/app/public/uploads/images/detail/iyTlprNOQ9qhl2kUgY0DpP2GubNjwlzrU0wW7aP2.webp')")
# mycursor.execute("INSERT INTO user3 (species_name, pic_url) VALUES ('Ilex verticillata', 'https://cdn.shopify.com/s/files/1/0261/2523/8377/products/bunchberryrestock_1024x1024_2x_c7516b0a-cd21-480f-bb1c-b60478c71ca8_1555x.png?v=1643321869')")
# mycursor.execute("INSERT INTO user3 (species_name, pic_url) VALUES ('Cornus canadensis', 'https://www.gardenia.net/storage/app/public/uploads/images/detail/iyTlprNOQ9qhl2kUgY0DpP2GubNjwlzrU0wW7aP2.webp')")
# mycursor.execute("INSERT INTO user3 (species_name, pic_url) VALUES ('Ilex verticillata', 'https://cdn.shopify.com/s/files/1/0261/2523/8377/products/bunchberryrestock_1024x1024_2x_c7516b0a-cd21-480f-bb1c-b60478c71ca8_1555x.png?v=1643321869')")
# conn.commit()
# #For testing
# mycursor.execute("SELECT * FROM userInfo")
# print(mycursor.fetchall())
# print('asdasdsaas')

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
# print(mycursor.fetchall())


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

# update_leaderBoard(1, 6222)
# update_leaderBoard(3, -6222)
# update_leaderBoard(2, 1500)
def top_ten_leaderboard():
    # sort the table first based on score
    sql4 = '''SELECT user_id, score
    FROM leaderBoard
    ORDER BY score DESC
    LIMIT 10'''
    mycursor.execute(sql4)
    return mycursor.fetchall()


# get list of all picture URLS stored in this user's table
def get_picURLs(user_id):
    # select pic_URLS where user_id = {user_id}
    sql5 = f"SELECT pic_URL FROM user{str(user_id)}"
    mycursor.execute(sql5)
    return mycursor.fetchall()

# "TODO: user has enough money: user table, parameters(username, donation_amount) -> bool":
def enough_money(username, donation_amount) -> bool:
    conn = sqlite3.connect('mydatabase.db')
    mycursor = conn.cursor()
    sql6 = f"SELECT money FROM userInfo WHERE username = '{username}'"
    mycursor.execute(sql6)
    return mycursor.fetchall()[0][0] >= donation_amount


# "TODO2: remove money from user: user table, parameters(username, donation_amount) -> None"
def remove_money(username, donation_amount):
    conn = sqlite3.connect('mydatabase.db')
    mycursor = conn.cursor()
    sql7 = f"SELECT money FROM userInfo WHERE username = '{username}'"
    mycursor.execute(sql7)
    data = mycursor.fetchone()
    minus_money = data[0] - donation_amount
 
    sql8 = f'''
            UPDATE userInfo
            SET money = '{minus_money}'
            WHERE username = '{username}'
            '''
    mycursor.execute(sql8)
    conn.commit()

# remove_money('varun', 200)


########################ERROR HERE (TODO2 test)####################################################################################
# remove_money('varun', 3000)
# sql = f"SELECT money FROM userInfo WHERE username = 'varun'"
# mycursor.execute(sql)
# print(mycursor.fetchall())
###################################################################################################################################

# "TODO3: add found score to user score in leaderboard: leaderboard, parameters(username, found_score) -> None"
def add_found_score(user_id, found_score):
    conn = sqlite3.connect('mydatabase.db')
    mycursor = conn.cursor()
    sql_88 = f"SELECT score FROM leaderBoard WHERE user_id = {user_id}"
    mycursor.execute(sql_88)
    data = mycursor.fetchone()
    add_score = data[0] + found_score
    sql9 = f'''
            UPDATE leaderBoard
            SET score = {add_score}
            WHERE user_id = {user_id}
            '''
    mycursor.execute(sql9)
# add_found_score(3, -4722)
def calc_user_progress(user_id, challenges: list):
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    cursor.execute(f'SELECT species_name FROM user{user_id}')
    data = set(cursor.fetchall())
    completed = []
    for species in challenges:
        if species in data:
            completed.append('Species Found!')
        else:
            completed.append('Species Currently Not Found...')
    return completed





conn.commit()

