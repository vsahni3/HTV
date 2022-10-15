import sqlite3

conn = sqlite3.connect('mydatabase.db')
mycursor = conn.cursor()


def update_user(user_id: int, species_name: str, pic_url: str):
    # create a table for this user if it doesn't already exist
    # user_id -> pic_id
    sql1 = f"CREATE TABLE IF NOT EXISTS user{str(user_id)} (pic_id INTEGER PRIMARY KEY AUTOINCREMENT, species_name nvarchar(100), pic_url nvarchar(200))"
    mycursor.execute(sql1)

    # inserts the user_id, species_name, pic_url
    sql = f"INSERT INTO user{str(user_id)} (species_name, pic_url) VALUES ('{species_name}', '{pic_url}')"
    mycursor.execute(sql)
    conn.commit()

update_user(69, 'hong', 'sexy')
mycursor.execute("SELECT * FROM user69")
print(mycursor.fetchall())
