import sqlite3


conn = sqlite3.connect("attributes.db")

cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Subjects')
cur.execute('DROP TABLE IF EXISTS Resources')
cur.execute('DROP TABLE IF EXISTS Passwords')

# Subjects table
cur.execute('''CREATE TABLE IF NOT EXISTS Subjects (
                uid TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                role TEXT NOT NULL,
                department TEXT NULL,
                subdepartment TEXT NULL,
                is_chair BOOLEAN NULL,
                courses_taught TEXT NULL,
                courses_taken TEXT NULL
            )''')


# Resources table
cur.execute('''CREATE TABLE IF NOT EXISTS Resources (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                owner TEXT null,
                type TEXT not null,
                subject TEXT,
                departments TEXT,
                courses TEXT
            )''')

# Passwords table
cur.execute('''CREATE TABLE IF NOT EXISTS Passwords (
                uid TEXT PRIMARY KEY,
                salted_hash TEXT
            )''')



conn.commit()
conn.close()
print("Tables dropped and re-created successfully.")