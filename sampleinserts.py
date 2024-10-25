import sqlite3

conn = sqlite3.connect('attributes.db')
cur = conn.cursor()


# List of tables to truncate
tables = ['Subjects', 'Resources', 'Passwords']

# Truncate each table (delete all rows)
for table in tables:
    cur.execute(f"DELETE FROM {table};")
    print(f"All rows from table {table} have been deleted.")

# Commit the changes
conn.commit()


# Generated sample inserts
cur.execute("INSERT INTO Subjects (uid, name, role, department, subdepartment, is_chair, courses_taught, courses_taken) VALUES ('AJohnson', 'Alice Johnson', 'professor', 'ecs', 'cs', 1, 'ecs_201, ecs_235', NULL);")
cur.execute("INSERT INTO Subjects (uid, name, role, department, subdepartment, is_chair, courses_taught, courses_taken) VALUES ('BSmith', 'Bob Smith', 'student', 'math', 'algebra', 0, NULL, 'ecs_201, math_120');")
cur.execute("INSERT INTO Subjects (uid, name, role, department, subdepartment, is_chair, courses_taught, courses_taken) VALUES ('CLee', 'Carol Lee', 'professor', 'cs', 'ai', 1, 'cs_420', NULL);")
cur.execute("INSERT INTO Subjects (uid, name, role, department, subdepartment, is_chair, courses_taught, courses_taken) VALUES ('DKim', 'David Kim', 'student', 'cs', 'ml', 0, NULL, 'cs_101, ecs_201');")
cur.execute("INSERT INTO Subjects (uid, name, role, department, subdepartment, is_chair, courses_taught, courses_taken) VALUES ('EBrown', 'Eva Brown', 'chair', 'math', NULL, 1, 'math_101, math_201', NULL);")
cur.execute("INSERT INTO Subjects (uid, name, role, department, subdepartment, is_chair, courses_taught, courses_taken) VALUES ('FWhite', 'Frank White', 'professor', 'ecs', 'networks', 0, 'ecs_235', NULL);")
cur.execute("INSERT INTO Subjects (uid, name, role, department, subdepartment, is_chair, courses_taught, courses_taken) VALUES ('GGreen', 'Grace Green', 'student', 'math', 'calculus', 0, NULL, 'math_101, math_102');")
cur.execute("INSERT INTO Subjects (uid, name, role, department, subdepartment, is_chair, courses_taught, courses_taken) VALUES ('HYoung', 'Henry Young', 'professor', 'cs', 'db', 0, 'cs_101', NULL);")
cur.execute("INSERT INTO Subjects (uid, name, role, department, subdepartment, is_chair, courses_taught, courses_taken) VALUES ('IScott', 'Ivy Scott', 'student', 'cs', 'ai', 0, NULL, 'cs_101');")
cur.execute("INSERT INTO Subjects (uid, name, role, department, subdepartment, is_chair, courses_taught, courses_taken) VALUES ('JBlack', 'Jack Black', 'professor', 'cs', 'ml', 1, 'cs_520', NULL);")
cur.execute("INSERT INTO Subjects (uid, name, role, department, subdepartment, is_chair, courses_taught, courses_taken) VALUES ('KMiller', 'Karen Miller', 'chair', 'cs', NULL, 1, 'cs_420', NULL);")
cur.execute("INSERT INTO Subjects (uid, name, role, department, subdepartment, is_chair, courses_taught, courses_taken) VALUES ('LTurner', 'Leo Turner', 'student', 'ecs', 'networks', 0, NULL, 'ecs_235');")
cur.execute("INSERT INTO Subjects (uid, name, role, department, subdepartment, is_chair, courses_taught, courses_taken) VALUES ('MLee', 'Maria Lee', 'student', 'cs', 'ml', 0, NULL, 'cs_520');")
cur.execute("INSERT INTO Subjects (uid, name, role, department, subdepartment, is_chair, courses_taught, courses_taken) VALUES ('NYoung', 'Nick Young', 'professor', 'math', 'stats', 1, 'math_120', NULL);")
cur.execute("INSERT INTO Subjects (uid, name, role, department, subdepartment, is_chair, courses_taught, courses_taken) VALUES ('OWhite', 'Olivia White', 'student', 'cs', 'security', 0, NULL, 'ecs_201, cs_420');")
cur.execute("INSERT INTO Subjects (uid, name, role, department, subdepartment, is_chair, courses_taught, courses_taken) VALUES ('PAdams', 'Paul Adams', 'professor', 'cs', 'security', 0, 'cs_101', NULL);")
cur.execute("INSERT INTO Subjects (uid, name, role, department, subdepartment, is_chair, courses_taught, courses_taken) VALUES ('QJones', 'Quincy Jones', 'student', 'cs', 'db', 0, NULL, 'cs_101, cs_520');")
cur.execute("INSERT INTO Subjects (uid, name, role, department, subdepartment, is_chair, courses_taught, courses_taken) VALUES ('RGrey', 'Rachel Grey', 'chair', 'ecs', NULL, 1, 'ecs_201', NULL);")
cur.execute("INSERT INTO Subjects (uid, name, role, department, subdepartment, is_chair, courses_taught, courses_taken) VALUES ('SHill', 'Sam Hill', 'professor', 'math', 'calculus', 0, 'math_102', NULL);")
cur.execute("INSERT INTO Subjects (uid, name, role, department, subdepartment, is_chair, courses_taught, courses_taken) VALUES ('TKing', 'Tina King', 'student', 'cs', 'ai', 0, NULL, 'cs_420');")

print("Samples inserted into Subjects")

cur.execute("INSERT INTO Resources (type, student, departments, courses) VALUES ('gradebook', 'Alice Johnson', 'ecs', 'ecs_201');")
cur.execute("INSERT INTO Resources (type, student, departments, courses) VALUES ('gradebook', 'Bob Smith', 'math', 'ecs_201');")
cur.execute("INSERT INTO Resources (type, student, departments, courses) VALUES ('exam', 'Carol Lee', 'cs', 'cs_420');")
cur.execute("INSERT INTO Resources (type, student, departments, courses) VALUES ('transcript', 'David Kim', 'cs', 'cs_101');")
cur.execute("INSERT INTO Resources (type, student, departments, courses) VALUES ('gradebook', 'Eva Brown', 'math', 'math_101');")
cur.execute("INSERT INTO Resources (type, student, departments, courses) VALUES ('assignment', 'Frank White', 'ecs', 'ecs_235');")
cur.execute("INSERT INTO Resources (type, student, departments, courses) VALUES ('exam', 'Grace Green', 'math', 'math_102');")
cur.execute("INSERT INTO Resources (type, student, departments, courses) VALUES ('syllabus', 'Henry Young', 'cs', 'cs_101');")
cur.execute("INSERT INTO Resources (type, student, departments, courses) VALUES ('transcript', 'Ivy Scott', 'cs', 'cs_101');")
cur.execute("INSERT INTO Resources (type, student, departments, courses) VALUES ('assignment', 'Jack Black', 'cs', 'cs_520');")
cur.execute("INSERT INTO Resources (type, student, departments, courses) VALUES ('gradebook', 'Karen Miller', 'cs', 'cs_420');")
cur.execute("INSERT INTO Resources (type, student, departments, courses) VALUES ('assignment', 'Leo Turner', 'ecs', 'ecs_235');")
cur.execute("INSERT INTO Resources (type, student, departments, courses) VALUES ('exam', 'Maria Lee', 'cs', 'cs_520');")
cur.execute("INSERT INTO Resources (type, student, departments, courses) VALUES ('syllabus', 'Nick Young', 'math', 'math_120');")
cur.execute("INSERT INTO Resources (type, student, departments, courses) VALUES ('transcript', 'Olivia White', 'cs', 'cs_420');")
cur.execute("INSERT INTO Resources (type, student, departments, courses) VALUES ('gradebook', 'Paul Adams', 'cs', 'cs_101');")
cur.execute("INSERT INTO Resources (type, student, departments, courses) VALUES ('exam', 'Quincy Jones', 'cs', 'cs_101');")
cur.execute("INSERT INTO Resources (type, student, departments, courses) VALUES ('transcript', 'Rachel Grey', 'ecs', 'ecs_201');")
cur.execute("INSERT INTO Resources (type, student, departments, courses) VALUES ('assignment', 'Sam Hill', 'math', 'math_102');")
cur.execute("INSERT INTO Resources (type, student, departments, courses) VALUES ('exam', 'Tina King', 'cs', 'cs_420');")

print("Samples inserted into Resources")