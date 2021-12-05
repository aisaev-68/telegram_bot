# -*- coding: utf-8 -*-

import sqlite3
from sqlite3 import Error
import logging
from datetime import datetime


def sql_connection():
    try:
        con = sqlite3.connect('data.db')
        return con
    except Error:
        logging.error(f"{datetime.now()} - {Error}")


def sql_table(con) -> None:
    cur = con.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS users(user_id INTEGER, name TEXT, command TEXT, date TEXT, hotels TEXT);")
    con.commit()


def sql_insert(con, entities: tuple) -> None:
    cur = con.cursor()
    cur.execute("INSERT INTO users (user_id, name, command, date, hotels) VALUES(?, ?, ?, ?, ?);", entities)
    con.commit()


def sql_fetch(con, id: int) -> list:
    """Функция выборки истории запросов и ответов из базы (последние 2 записи пользователя)"""
    cur = con.cursor()
    cur.execute(f"SELECT command, date, hotels FROM users WHERE user_id ={id} ORDER BY rowid DESC LIMIT 2;")
    rows = cur.fetchall()

    return rows


def sql_fetch_del(con) -> None:
    cur = con.cursor()
    cur.execute('DROP TABLE if exists users;')
    con.commit()
    con.close()
