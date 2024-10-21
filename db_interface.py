import sqlite3

conn = sqlite3.connect('attributes.db')
cur = conn.cursor()


def add_subject(subject):
    if subject.role is "admin":
        try:
            cur.execute('''INSERT INTO Subjects (uid, name, role, department) VALUES (?, ?, ?, ?)'''
                                (subject.uid, subject.name, "admin", subject.department))
            conn.commit()
        except:
            print("Error inserting subject")
    elif subject.role is "chancellor":
        try:
            cur.execute('''INSERT INTO Subjects (uid, name, role, department) VALUES (?, ?, ?, ?)'''
                                (subject.uid, subject.name, "chancellor", subject.department))
            conn.commit()
        except:
            print("Error inserting subject")
    elif subject.role is "staff":
        try:
            cur.execute('''INSERT INTO Subjects (uid, name, role, department) VALUES (?, ?, ?, ?)'''
                                (subject.uid, subject.name, "staff", subject.department))
            conn.commit()
        except:
            print("Error inserting subject")
    elif subject.role is "professor":
        try:
            cur.execute('''INSERT INTO Subjects (uid, name, role, department) VALUES (?, ?, ?, ?)'''
                                (subject.uid, subject.name, "professor", subject.department))
            conn.commit()
        except:
            print("Error inserting subject")
    elif subject.role is "student":
        try:
            cur.execute('''INSERT INTO Subjects (uid, name, role, department) VALUES (?, ?, ?, ?)'''
                                (subject.uid, subject.name, "student", subject.department))
            conn.commit()
        except:
            print("Error inserting subject")
    else:
        print("Unknown role")

def add_resource(resource):
    if resource.student is not None:
        cur.execute('''SELECT uid FROM Subjects WHERE name = ?''', (resource.student,))
        student = cur.fetchone()
        if student:
            cur.execute('''INSERT INTO Resources (type, student, departments, courses) 
                        VALUES (?, ?,  ?, ?)''', 
                        (resource.type, student[0], resource.departments, resource.courses))
            conn.commit()
            print(f"Resource {resource.type} added for {resource.student}")
        else:
            print("Student not found.")
    
    elif resource.courses is None:
        cur.execute('''INSERT INTO Resources (type, departments) 
                        VALUES (?, ?)''', (resource.type, resource.departments))
        conn.commit()
        print(f"Resource {resource.type} added")
    
    else:
        cur.execute('''INSERT INTO Resources (type, departments, courses) 
                        VALUES (?, ?, ?)''', (resource.type, resource.departments, resource.courses))
        conn.commit()
        print(f"Resource {resource.type} added")

def subject_row(uid):
    query = f"SELECT TOP(1) FROM Subjects where uid = {uid}"
    cur.execute(query)
    rows = cur.fetchone() 
    return rows

def resource_row(id):
    query = f"SELECT TOP(1) FROM Resources where uid = {id}"
    cur.execute(query)
    rows = cur.fetchone() 
    return rows

def password_row(uid):
    query = f"SELECT TOP(1) FROM Passwords where uid = {uid}"
    cur.execute(query)
    rows = cur.fetchone() 
    return rows
