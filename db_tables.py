import sqlite3


conn = sqlite3.connect("attributes.db")

cur = conn.cursor()

# Subjects table
cur.execute('''CREATE TABLE IF NOT EXISTS Subjects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                role TEXT,
                department TEXT,
                subdepartment TEXT,
                is_chair BOOLEAN,
                courses_taught TEXT,
                courses_taken TEXT
            )''')

# Departments table
cur.execute('''CREATE TABLE IF NOT EXISTS Departments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE,
                chair_id INTEGER,
                FOREIGN KEY(chair_id) REFERENCES Subjects(id)
            )''')

# Courses table
cur.execute('''CREATE TABLE IF NOT EXISTS Courses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT UNIQUE,
                department_id INTEGER,
                professor_id INTEGER,
                FOREIGN KEY(department_id) REFERENCES Departments(id),
                FOREIGN KEY(professor_id) REFERENCES Subjects(id)
            )''')

# Resources table
cur.execute('''CREATE TABLE IF NOT EXISTS Resources (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT,
                student_id INTEGER,
                department_id INTEGER,
                course_id INTEGER,
                FOREIGN KEY(student_id) REFERENCES Subjects(id),
                FOREIGN KEY(department_id) REFERENCES Departments(id),
                FOREIGN KEY(course_id) REFERENCES Courses(id)
            )''')

# Rules table
cur.execute('''CREATE TABLE IF NOT EXISTS Rules (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject_role TEXT,
                resource_type TEXT,
                constraint TEXT
            )''')



conn.commit()
conn.close()