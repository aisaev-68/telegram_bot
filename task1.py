import sqlite3
from sqlite3 import Error

def sql_connection():
    try:
        con = sqlite3.connect('data.db')
        return con
    except Error:
        print(Error)

def sql_table(con):
    cursorObj = con.cursor()
    cursorObj.execute("CREATE TABLE if not exists users(user_id integer PRIMARY KEY, "
                      "username text, search_city text, chat_id integer, id_city text, "
                      "checkIn text, checkOut text, count_show_hotels integer, "
                      "count_show_photo integer, price_min integer, price_max integer, "
                      "distance_min integer, distance_max integer, language text, "
                      "currency text, diff_date integer, mes_id_hotel integer, "
                      "mes_id_photo integer, search_hotels integer)")
    con.commit()


def sql_insert(con, entities):
    cursorObj = con.cursor()
    cursorObj.execute("INSERT INTO users(user_id, username, search_city, chat_id, id_city, "
                      "checkIn, checkOut, count_show_hotels, count_show_photo, price_min, "
                      "price_max, distance_min, distance_max, language, currency, diff_date, "
                      "mes_id_hotel, mes_id_photo, search_hotels) "
                      "VALUES(?, ?, ?, ?, ?, ?)", entities)
    con.commit()

def sql_update(con):
    cursorObj = con.cursor()
    cursorObj.execute('UPDATE users SET username = "Rogers" where user_id = 2')
    con.commit()

def sql_fetch(con):
    cursorObj = con.cursor()
    cursorObj.execute('SELECT * FROM users')
    rows = cursorObj.fetchall()
    for row in rows:
        print(row)

def sql_fetch_del(con):
    cursorObj = con.cursor()
    cursorObj.execute('DROP table if exists users')
    con.commit()



entities = (2, 'Andrew', 800, 'IT', 'Tech', '2018-02-06')


con = sql_connection()
sql_table(con)
# sql_insert(con, entities)
# sql_update(con)
# sql_fetch(con)
con.close()
