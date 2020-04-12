import sqlite3
import configparser

# Config reader
config = configparser.ConfigParser()
config.read("config.ini")


class ErepDB:
    _db_connection = None
    _db_cur = None

    def __init__(self):
        self._db_connection = sqlite3.connect(config["DEFAULT"]["db_name"])
        self._db_cur = self._db_connection.cursor()

    def queryone(self, query, params):
        self._db_cur.execute(query, params)
        return self._db_cur.fetchone()

    def queryall(self, query, params):
        self._db_cur.execute(query, params)
        return self._db_cur.fetchall()

    def __del__(self):
        self._db_connection.close()
