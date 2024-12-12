import os, hashlib, sqlite3, sys, base64, platform, subprocess
from db.db_interface import subject_row, add_password, add_resource
from utils.entities import FILE_TYPES, DEPARTMENTS, Subject, Resource
from utils.ruleset import check_your_privilege
from getpass import getpass

conn=sqlite3.connect('db/attributes.db')
cur=conn.cursor()

def set_metadata(path, identifier):
    try:
        if platform.system() == "Darwin":  # macOS
            subprocess.run(["xattr", "-w", 'id', identifier, path], check=True)
        else:  # Linux
            subprocess.run(["setfattr", "-n", 'id', "-v", identifier, path], check=True)
        # print(f"Successfully set id to {identifier} on {path}")
    except Exception as e:
        print(f'Error: {e}')

def get_metadata(path):
    try:
        if platform.system() == "Darwin":  # macOS
            result = subprocess.run(["xattr", "-p", "id", path], capture_output=True, text=True)
        else:  # Linux
            result = subprocess.run(["getfattr", "-n", "id", "--only-values", path], capture_output=True, text=True)
        
        return result.stdout.strip()
    except Exception as e:
        print(f'Error: {e}')
    
def create_resource(sub, path, user_file=False):
    """
    This function implements the interface for creating resources of specific types. The resource
    is first built based on user selections and is then tested against the subject for execute 
    permissions. If execute, then the resource can be created. This allows for granularity in who
    can create what resource. It takes a Subject(), path or name, and argument for simple userfile 
    creation. It returns a Resource and a flag. 
    """
    res = Resource(name=path, owner=sub.id)
    flag = False
    if not user_file:
        print(f"Select resource type to create:")
        for i, type in enumerate(FILE_TYPES):
            print(f'{i}. {type}')
        try:
            num = int(input('> '))
            if num >= 0 and num <= len(FILE_TYPES):
                if num == 0: # grade book 
                    course_list = list(sub.courses_taught)
                    print(f"Select course (0-{len(course_list) - 1}):")
                    # convert set to list for indexing
                    for i, course in enumerate(course_list):
                        print(f'{i}. {course}')
                    num = int(input('> '))
                    if num >= 0 and num <= len(sub.courses_taught):
                        res.type = 'gradebook'
                        res.courses = {course_list[num]}
                        flag = True
                    else:
                        print('Invalid selection')

                elif num == 1: # transcript
                    uid = input("Enter student's uid: ")
                    student = subject_row(uid)
                    if student.id != '':
                        res.type = 'transcript'
                        res.subject = uid
                        flag = True

                elif num == 2: # finacial record
                    # list the departments for selection
                    print(f'Select department (0-{len(DEPARTMENTS) - 1})')
                    for i, dept in enumerate(DEPARTMENTS):
                        print(f'{i}. {dept}')
                    num = int(input('> '))
                    if num >= 0 and num <= len(DEPARTMENTS):
                       dept = DEPARTMENTS[num] 
                    else:
                        print('Invalid selection')

                    # chose a student that existsa
                    id = input('Enter students ID: ')
                    student = subject_row(id)
                    if student.id != '':
                        res.type = 'finacial_record'
                        res.departments = {dept}
                        res.subject = id
                        flag = True

                elif num == 3: # donor record
                    subdepartments = list(sub.subdepartments)
                    print(f"Select subdepartment (0-{len(subdepartments) - 1})")
                    for i, subdept in enumerate(subdepartments):
                        print(f'{i}. {subdept}')
                    num = int(input('> '))
                    if num >= 0 and num <= len(subdepartments):
                        res.type = 'donor_record'
                        res.departments = {subdepartments[num]}
                        flag = True
                    else:
                        print('Invalid selection')

                else: # user file
                    res.type = 'user_file'
                    flag = True
            else:
                print('Invalid selection')
        except ValueError as e:
            print(f'Error: invalid selection')
    else:
        res.type = 'user_file'
        flag = True
    
    # run the check to determine permissions
    read, write, execute, own = check_your_privilege(sub, res)
    if execute and flag:
        return res, True
    else:
        return res, False

def create_file(path, sub, touch=False):
    if not os.path.exists(path):
        # create a resource. If you are a guest or if 'touch' was used, simply create a user_file
        if touch or sub.role == 'guest':
            res, flag = create_resource(sub, path, user_file=True)
        else:
            res, flag = create_resource(sub, path)     
        if flag:   
            try:
                # create an actual file
                with open(path, 'w') as file:
                    file.write("")
                res_id = add_resource(res)
                set_metadata(path=path, identifier=str(res_id))
                return True
            except Exception as e:
                print(e)
                # print("Error: file was not created.")
                return False
        else:
            return
    else:
        print("Error: file already exists")

def load_file(path, res):
    with open(path, 'w') as file:
        file.write(f"{res}")
    set_metadata(path=path, identifier=str(res.id))

def verify_password(password, salt):
    # Decode the Base64 encoded salt
    salt_bytes = base64.b64decode(salt)
    hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt_bytes, 100000)
    return base64.b64encode(hashed_password).decode('utf-8')

def hash_password(password, uname):
    # Generate a salt using a combination of username and random bytes
    salt = hashlib.sha256(uname.encode('utf-8') + os.urandom(16)).digest()
    hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return base64.b64encode(hashed_password).decode('utf-8'), base64.b64encode(salt).decode('utf-8')

def user_exists(user):
        cur.execute('''SELECT id FROM Passwords WHERE id = ?''', (user,))
        username=cur.fetchone()
        if username:
            return True
        return False

def authenticate_user(username, password):
    cur.execute('''SELECT id,salted_hash,salt from Passwords WHERE id=?''',(username,))
    result= cur.fetchone()
    if result:
        id,salted_hash,salt = result
        entered_pass_hash = verify_password(password, salt)
        if salted_hash == entered_pass_hash:
           return True
        else:
            print("Password incorrect")
            return False

def login():
    for i in range(3):
        uname = input("Enter username: ")
        if not user_exists(uname):
            print("User does not exist.")
            continue
        
        if uname != 'guest':
            pwd = getpass("Password: ")
            if not authenticate_user(uname, pwd):
                print("Incorrect password.")
                continue
            else:
                print("Login successful.")
                subject = subject_row(uname)
                return subject
        else:
            print("Login successful.")
            subject = subject_row(uname)
            return subject
    print('Exeeded maximum tries. Exiting...')
    sys.exit()

# def register():
#     uname = input("Enter your username")
        
#     if user_exists(uname):
#             print("Username already exists")
#             return     

#     # setting the rules of the password
#     PUNCTUATIONS = "@#$%&"
#     DEFAULT_PASSWORD_LENGTH = 12


#     password = input("Enter a password. \n 1. Password must be between 12 to 16 characters. \n 2.Password must contain special characters: @#$%&.\n ") # Create a condition so they can't use their name or school name in the password.

#     if len(password)<12 or len(password)> 16:
#             print('Password length must be between 12 and 16.')
#             return

#     hpwd,salt = hash_password(password)
#     add_password(uname, )

