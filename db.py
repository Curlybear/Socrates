import sqlite3
import csv
import re

conn = sqlite3.connect('erep.db')
c = conn.cursor()

c.execute('CREATE TABLE users(username text, id real, discordusername text, PRIMARY KEY(username))')
c.execute("CREATE INDEX index_user_id ON users (id);")
c.execute('''CREATE TABLE countries(id real, name text, flag text, PRIMARY KEY(id))''')

with open("users.csv", "r", encoding="latin-1") as f:
	for row in csv.reader(f, delimiter=';', skipinitialspace=True):
		if row[0].isnumeric() and row[1] != '\'':
			c.execute("INSERT OR IGNORE INTO users VALUES (?, ?, ?)", (row[1], row[0], ''))
print('Done Users!')

with open("countries.csv", "r", encoding="latin-1") as f:
	for row in csv.reader(f, delimiter=';', skipinitialspace=True):
		c.execute("INSERT INTO countries VALUES (?, ?, ?)", (row[0], row[1], row[2]))
print('Done Countries!')

conn.commit()
conn.close()