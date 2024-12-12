import sqlite3
from utils.utils import hash_password, load_file
from utils.organization import SUBJECTS_LIST, PASSWORD_LIST, RESOURCE_LIST
from utils.entities import COMMANDS
from db.db_interface import add_subject, add_resource, add_password, print_table, resource_row

conn = sqlite3.connect("db/attributes.db")
cur = conn.cursor()

def load_organization():
    cur.execute('DROP TABLE IF EXISTS Subjects')
    cur.execute('DROP TABLE IF EXISTS Resources')
    cur.execute('DROP TABLE IF EXISTS Passwords')

    # Subjects table
    cur.execute('''CREATE TABLE IF NOT EXISTS Subjects (
                    id TEXT PRIMARY KEY,
                    name TEXT NULL,
                    role TEXT NULL,
                    departments TEXT NULL,
                    subdepartments TEXT NUL,
                    is_chair BOOLEAN NULL,
                    courses_taught TEXT NULL,
                    courses_taken TEXT NULL
                )''')


    # Resources table
    cur.execute('''CREATE TABLE IF NOT EXISTS Resources (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT null, 
                    owner TEXT null,
                    type TEXT not null,
                    subject TEXT,
                    departments TEXT,
                    courses TEXT
                )''')

    # Passwords table
    cur.execute('''CREATE TABLE IF NOT EXISTS Passwords (
                    id TEXT PRIMARY KEY,
                    salted_hash TEXT,
                    salt TEXT
                )''')

    for i, sub in enumerate(SUBJECTS_LIST):
        try:
            # add the user attributes and hashed passwords and salts 
            add_subject(sub)
            password, salt = hash_password(PASSWORD_LIST[i], sub.id)
            add_password(sub.id, password, salt)
        except Exception as e:
            print(e)

    print_table('Subjects')
    print_table('Passwords')
    for res in RESOURCE_LIST:
        # We don't store commands in the db, we simply generate those resources on the fly
        if res.type not in COMMANDS:
            res.id = add_resource(res)
            load_file(res.name, res)
        

    print_table('Resources')

    print("Tables dropped and re-created successfully.")
    conn.commit()
    conn.close()
