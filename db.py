import sqlite3
import csv
import configparser

# Config reader
config = configparser.ConfigParser()
config.read("config.ini")

conn = sqlite3.connect(config["DEFAULT"]["db_name"])
c = conn.cursor()

c.execute("CREATE TABLE countries(id REAL, name TEXT, flag TEXT, PRIMARY KEY(id))")

with open("countries.csv", "r", encoding="latin-1") as f:
    for row in csv.reader(f, delimiter=";", skipinitialspace=True):
        c.execute("INSERT INTO countries VALUES (?, ?, ?)", (row[0], row[1], row[2]))
print("Done Countries!")

conn.commit()
conn.close()
