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
    if resource.subject != None:
        # we need to match the sub id with res id. 
        cur.execute('''SELECT uid FROM Subjects WHERE uid = ?''', (resource.subject,))
        subject = cur.fetchone()
        if subject:
            cur.execute('''INSERT INTO Resources (id, owner, type, subject, departments, courses) 
                        VALUES (?, ?,  ?, ?)''', 
                        (resource.id, resource.owner, resource.type, subject[0], resource.departments, resource.courses))
            conn.commit()
            print(f"Resource {resource.type} added for {resource.subject}")
            res_id = cur.lastrowid  # Retrieve the ID of the newly inserted row
            return res_id
        else:
            print("Student not found.")
            return None
    
    elif resource.courses == None:
        cur.execute('''INSERT INTO Resources (type, departments) 
                        VALUES (?, ?)''', (resource.type, resource.departments))
        conn.commit()
        print(f"Resource {resource.type} added")
        res_id = cur.lastrowid
        return res_id
    else:
        cur.execute('''INSERT INTO Resources (type, departments, courses) 
                        VALUES (?, ?, ?)''', (resource.type, resource.departments, resource.courses))
        conn.commit()
        print(f"Resource {resource.type} added")
        res_id = cur.lastrowid
        return res_id

def subject_row(uid):
    query = "SELECT * FROM Subjects WHERE uid = ? LIMIT 1"
    cur.execute(query, (uid,))
    rows = cur.fetchone() 
    return rows

def resource_row(id): # TODO: continue to ensure the ids are the ones saved and returned, and not the names
    query = "SELECT * FROM Resources WHERE id = ? LIMIT 1"
    cur.execute(query, (id,))
    rows = cur.fetchone() 
    return rows

def password_row(uid):
    query = "SELECT * FROM Passwords WHERE uid = ? LIMIT 1"
    cur.execute(query, (uid,))
    rows = cur.fetchone() 
    return rows
