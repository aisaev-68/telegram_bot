import sqlite3
from sqlite3 import Error
from botrequests.handlers import logging
from datetime import datetime

def sql_connection():
    try:
        con = sqlite3.connect('data.db')
        return con
    except Error:
        logging.error(f"{datetime.now()} - {Error}")

def sql_table(con):
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS users(user_id integer PRIMARY KEY,"
                      "username text, command text, date text, hotels text(2000));""")
    con.commit()


def sql_insert(con, entities):
    cur = con.cursor()
    cur.execute(f"""INSERT INTO users(user_id, username, command, date, hotels) 
    VALUES{entities};""")
    con.commit()
    con.close()

def sql_update(con, entities):
    cur = con.cursor()
    cur.execute(f"UPDATE users SET command={entities[1]}, date={entities[2]}, "
                f"hotels={entities[3]} WHERE user_id ={entities[0]};")
    con.commit()
    con.close()

def sql_fetch(con, id: int):
    cur = con.cursor()
    cur.execute(f'SELECT command, date, hotels FROM users WHERE user_id ={id};')
    rows = con.fetchall()
    con.close()
    return rows

def sql_fetch_del(con):
    cur = con.cursor()
    cur.execute('DROP TABLE if exists users;')
    con.commit()
    con.close()



#entities = (2, 'Andrew', 800, 'IT', 'Tech', '2018-02-06')


# con = sql_connection()
# sql_table(con)
# sql_insert(con, entities)
# sql_update(con)
# sql_fetch(con)
#con.close()
