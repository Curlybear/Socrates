import csv
import configparser
import os
import psycopg2
import logging

import wikientries

logger = logging.getLogger('Socrates.'+__name__)


class DbManager:
    def __init__(self):
        # Config reader
        self.directory = os.path.dirname(__file__)
        filename = os.path.join(self.directory, 'config.ini')
        self.config = configparser.ConfigParser()
        self.config.read(filename)

        #DB
        self.db_conn = psycopg2.connect(host=self.config['DB']['host'], database=self.config['DB']['db_name'],
                                        user=self.config['DB']['user'], password=self.config['DB']['password'],
                                        port=self.config['DB']['port'])
        self.db_cur = self.db_conn.cursor()

    def __del__(self):
        self.db_cur.close()
        self.db_conn.close()

    def check_db(self):
        self.db_cur.execute("SELECT to_regclass('public.users');")
        res = self.db_cur.fetchone()

        if res[0] is None:
            return False
        else:
            return True

    def init_db(self):
        try:
            self.db_cur.execute("""CREATE TABLE users (
                                  id INT PRIMARY KEY,
                                  username TEXT,
                                  discordusername TEXT
                                  );""")
            self.db_cur.execute('CREATE INDEX username_index ON users(username);')
            self.db_cur.execute("""CREATE TABLE countries (
                                  id INT PRIMARY KEY,
                                  name TEXT,
                                  flag TEXT
                                  );""")
            self.db_cur.execute("""CREATE TABLE wiki (
                                  tag TEXT PRIMARY KEY,
                                  category TEXT,
                                  embed TEXT
                                  );""")
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            exit(-1)

    def load_users(self):
        filename = os.path.join(self.directory, 'users.csv')
        with open(filename, "r", encoding="latin-1") as f:
            for row in csv.reader(f, delimiter=';', skipinitialspace=True):
                if row[0].isnumeric() and row[1] != '\'':
                    self.db_cur.execute('INSERT INTO users(id, username, discordusername) VALUES (%s, %s, %s)', (row[0], row[1], ''))

    def load_countries(self):
        filename = os.path.join(self.directory, 'countries.csv')
        with open(filename, "r", encoding="latin-1") as f:
            for row in csv.reader(f, delimiter=';', skipinitialspace=True):
                self.db_cur.execute('INSERT INTO countries(id, name, flag) VALUES (%s, %s, %s)', (row[0], row[1], row[2]))

    def load_wiki_entries(self):
        embeds = wikientries.get_embeds()
        for em in embeds:
            self.db_cur.execute('INSERT INTO wiki(tag, category, embed) VALUES (%s,%s,%s)', (em[1], 'Alliance', em[0]))

    def queryone(self, query, params):
        self.db_cur.execute(query, params)
        return self.db_cur.fetchone()

    def queryall(self, query, params):
        self.db_cur.execute(query, params)
        return self.db_cur.fetchall()


def start_db():
    db = DbManager()
    if not db.check_db():
        db.init_db()
        db.load_users()
        logger.info('Users loaded in DB')
        db.load_countries()
        logger.info('Countries loaded in DB')
        db.load_wiki_entries()
        logger.info('Wiki entries loaded in DB')
        db.db_conn.commit()
