import sqlite3

conn = sqlite3.connect('attributes.db')
cur = conn.cursor()


def add_subject(subject):
    try:
        cur.execute('''INSERT INTO Subjects (uid, name, role, department) VALUES (?, ?, ?, ?)''',
                    (subject.uid, subject.name, subject.role, subject.department))
        conn.commit()
    except Exception as e:
        print(f"Error inserting subject: {e}")


def add_resource(resource):
    if resource.student != None:
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
    
    elif resource.courses == None:
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
    query = "SELECT * FROM Subjects WHERE uid = ? LIMIT 1"
    cur.execute(query, (uid,))
    rows = cur.fetchone() 
    return rows

def resource_row(id):
    query = "SELECT * FROM Resources WHERE id = ? LIMIT 1"
    cur.execute(query, (id,))
    rows = cur.fetchone() 
    return rows

def password_row(uid):
    query = "SELECT * FROM Passwords WHERE uid = ? LIMIT 1"
    cur.execute(query, (uid,))
    rows = cur.fetchone() 
    return rows
