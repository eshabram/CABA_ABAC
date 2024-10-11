import sqlite3
import os

con = sqlite3.connect("attributes.db")
cur = con.cursor()

if not os.path.isfile('attributes.db'):
    cur.execute("CREATE TABLE Policies (PolicyID INT PRIMARY KEY, PolicyName VARCHAR(255), Description TEXT)")
else:
    print('Db already created')

res = cur.execute("SELECT * FROM sqlite_master")

print(res)