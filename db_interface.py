import sqlite3

conn = sqlite3.connect('attributes.db')
cur = conn.cursor()


def add_subject(name, role, department, subdepartment, is_chair):
    cur.execute('''INSERT INTO Subjects (name, role, department, subdepartment, is_chair) 
                   VALUES (?, ?, ?, ?, ?)''', (name, role, department, subdepartment, is_chair))
    conn.commit()
    print(f"Subject {name} added with role {role}")

def assign_course(subject_name, course_code, teaching_or_taking):
    cur.execute('''SELECT id FROM Subjects WHERE name = ?''', (subject_name,))
    subject = cur.fetchone()
    if subject:
        cur.execute('''SELECT id FROM Courses WHERE code = ?''', (course_code,))
        course = cur.fetchone()
        if course:
            if teaching_or_taking == "teaching":
                cur.execute('''UPDATE Subjects SET courses_taught = ? WHERE id = ?''', 
                            (course_code, subject[0]))
            elif teaching_or_taking == "taking":
                cur.execute('''UPDATE Subjects SET courses_taken = ? WHERE id = ?''', 
                            (course_code, subject[0]))
            conn.commit()
            print(f"Course {course_code} assigned to {subject_name} as {teaching_or_taking}")
        else:
            print("Course not found.")
    else:
        print("Subject not found.")

def add_resource(resource_type, student_name, department, course_code):
    cur.execute('''SELECT id FROM Subjects WHERE name = ?''', (student_name,))
    student = cur.fetchone()
    if student:
        cur.execute('''INSERT INTO Resources (type, student_id, department_id, course_id) 
                       VALUES (?, ?, (SELECT id FROM Departments WHERE name = ?), 
                               (SELECT id FROM Courses WHERE code = ?))''', 
                    (resource_type, student[0], department, course_code))
        conn.commit()
        print(f"Resource {resource_type} added for {student_name}")
    else:
        print("Student not found.")

def create_rule(subject_role, resource_type, constraint):
    cur.execute('''INSERT INTO Rules (subject_role, resource_type, constraint) 
                   VALUES (?, ?, ?)''', (subject_role, resource_type, constraint))
    conn.commit()
    print(f"Rule added: {subject_role} can access {resource_type} with constraint {constraint}")

def all_from(table):
    query = f"SELECT * FROM {table}"
    cur.execute(query)
    rows = cur.fetchall()  # Fetch all rows from the table
    return rows

# UNDER CONSTRUCTION
# def evaluate_access(subject_name, resource_type):
#     cur.execute('''SELECT role, courses_taught FROM Subjects WHERE name = ?''', (subject_name,))
#     subject = cur.fetchone()
#     if subject:
#         role, courses_taught = subject
#         cur.execute('''SELECT constraint FROM Rules WHERE subject_role = ? AND resource_type = ?''', 
#                     (role, resource_type))
#         rule = cur.fetchone()
#         if rule:
#             constraint = rule[0]

#             if resource_type == 'gradebook' and 'ecs_235a' in courses_taught:
#                 print(f"Access granted to {subject_name} for {resource_type}")
#             else:
#                 print(f"Access denied to {subject_name} for {resource_type}")
#         else:
#             print("No matching rule found.")
#     else:
#         print("Subject not found.")