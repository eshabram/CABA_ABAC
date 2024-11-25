import sqlite3
from utils.entities import Subject, Resource

conn = sqlite3.connect('db/attributes.db')
cur = conn.cursor()

def add_subject(subject):
    """
    This function adds subjects to the Subjects table of the database. It first converts a fiew of the attributes
    for storage in the db. It takes a type Subject() param. 
    """
    try:
        # convert values for storage
        departments_str = ",".join(subject.departments) if subject.departments else None
        subdepartments_str = ",".join(subject.subdepartments) if subject.subdepartments else None
        courses_taught_str = ",".join(subject.courses_taught) if subject.courses_taught else None
        courses_taken_str = ",".join(subject.courses_taken) if subject.courses_taken else None
        is_chair = 1 if subject.is_chair else 0

        cur.execute('''INSERT INTO Subjects (id, role, departments, subdepartments, is_chair, courses_taught, courses_taken) VALUES (?, ?, ?, ?, ?, ?, ?)''',
                    (subject.id, subject.role, departments_str, subdepartments_str, is_chair, courses_taught_str, courses_taken_str))
        conn.commit()
    except Exception as e:
        print(f"Error inserting subject: {e}")

def add_resource(resource):
    try:
        # convert for storage in the db
        departments_str = ",".join(resource.departments) if resource.departments else None
        courses_str = ",".join(resource.courses) if resource.courses else None

        cur.execute('''INSERT INTO Resources (name, owner, type, subject, departments, courses) 
                    VALUES (?, ?, ?, ?, ?, ?)''', 
                    (resource.name, resource.owner, resource.type, resource.subject, departments_str, courses_str))
        conn.commit()
        print(f"Resource {resource.type} added for {resource.subject}")
        res_id = cur.lastrowid  # Retrieve the ID of the newly inserted row
        return res_id
    except Exception as e:
        print(e)
    
def add_password(uname, password, salt):
    try:
        cur.execute('''INSERT into Passwords(id,salted_hash,salt)
                VALUES(?,?,?)''',
                (uname, password, salt))
        conn.commit()
    except Exception as e:
        print(e)

def subject_row(id):
    query = "SELECT * FROM Subjects WHERE id = ? LIMIT 1"
    cur.execute(query, (id,))
    row = cur.fetchone() 

    if row:
        subject = Subject(
            id=row[0],
            role=row[1],
            departments=set(row[2].split(",")) if row[2] else set(),  # Convert back to set
            is_chair=bool(row[3]),  # Convert INTEGER to boolean
            courses_taught=set(row[4].split(",")) if row[4] else set(),  # Convert back to set
            courses_taken=set(row[5].split(",")) if row[5] else set()  # Convert back to set
        )
    else:
        print(f"No subject found with id {id}")
    return subject

def resource_row(id): # TODO: continue to ensure the ids are the ones saved and returned, and not the names
    query = "SELECT * FROM Resources WHERE id = ? LIMIT 1"
    cur.execute(query, (id,))
    row = cur.fetchone() 

    if row:
        resource = Resource(
            id=row[0],
            name=row[1],
            owner=row[2],
            type=row[3],
            subject=row[4],
            departments=set(row[5].split(",")) if row[5] else set(),  # Convert back to set
            courses=set(row[6].split(",")) if row[6] else set(),  # Convert back to set
        )
    return resource

def password_row(id):
    query = "SELECT * FROM Passwords WHERE id = ? LIMIT 1"
    cur.execute(query, (id,))
    rows = cur.fetchone() 
    return rows

def print_table(table):
    cur.execute(f"SELECT * FROM {table}")
    rows = cur.fetchall()

    print(f'\n{table}:')
    # Display the rows
    for i, row in enumerate(rows):
        print(f'{i}. {row}')
    print()

def pragma_table(table):
    cur.execute(f'PRAGMA table_info({table});')
    columns = cur.fetchall()

    # Print the table structure
    print(f"Table structure for {table}:")
    for column in columns:
        print(column)