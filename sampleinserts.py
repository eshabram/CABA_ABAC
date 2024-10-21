import sqlite3

conn = sqlite3.connect('attributes.db')
cur = conn.cursor()


# List of tables to truncate
tables = ['Subjects', 'Departments', 'Courses', 'Resources', 'Rules']

# Truncate each table (delete all rows)
for table in tables:
    cur.execute(f"DELETE FROM {table};")
    print(f"All rows from table {table} have been deleted.")

# Commit the changes
conn.commit()


# Generated sample inserts
cur.execute('''INSERT INTO Subjects (name, role, department, subdepartment, is_chair, courses_taught, courses_taken) 
               VALUES ('Alice Johnson', 'Professor', 'Computer Science', 'Software Engineering', 1, 'CS101, CS202', 'CS102, CS203')''')
cur.execute('''INSERT INTO Subjects (name, role, department, subdepartment, is_chair, courses_taught, courses_taken) 
               VALUES ('Bob Smith', 'Student', 'Computer Science', 'AI', 0, '', 'CS101, CS202')''')
cur.execute('''INSERT INTO Subjects (name, role, department, subdepartment, is_chair, courses_taught, courses_taken) 
               VALUES ('Catherine Davis', 'Professor', 'Mathematics', 'Statistics', 0, 'MATH101, MATH202', '')''')
print("Samples inserted into Subjects")
# Insert into Resources table
cur.execute('''INSERT INTO Resources (type, student_id, department_id, course_id) 
               VALUES ('Assignment', 2, 1, 1)''')
cur.execute('''INSERT INTO Resources (type, student_id, department_id, course_id) 
               VALUES ('Exam', 2, 1, 3)''')
print("Samples inserted into Resources")