import os, hashlib, sqlite3, sys, base64, platform, subprocess
from db.db_interface import subject_row, add_password, add_resource
from utils.entities import FILE_TYPES, Subject, Resource
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
    # TODO: we pass in subject so that we can run checks on what kinds of resources they can create
    if not user_file:
        print(f"Select resource type to create:")
        for i, type in enumerate(FILE_TYPES):
            print(f'{i}. {type}')
        try:
            num = int(input('> '))
            if num >= 0 and num <= len(FILE_TYPES):
                if num == 0 and sub.role in ['professor', 'admin']:
                    print('Select course:')
                    # convert set to list for indexing
                    course_list = sub.courses_taught
                    for i, course in enumerate(course_list):
                        print(f'{i}. {course}')
                    num = int(input('> '))
                    if num >= 0 and num <= len(sub.courses_taught):
                        return Resource(name=path, owner=sub.id, type='gradebook', courses={course_list[num]}), True
                    else:
                        print('Invalid selection')
                        return Resource(), False
                elif num == 1 and ('reg' in sub.departments or sub.role == 'admin'):
                    uid = input("Enter student's uid: ")
                    student = subject_row(uid)
                    if sub.id != '':
                        return Resource(name=path, owner=sub.id, type='transcript', subject=student.id), True 
                    else:
                        return Resource(), False
                elif num == 2 and ('fo' in sub.departments or sub.role == 'admin'):
                    return
                elif num == 3 and ('fo' in sub.departments or sub.role == 'admin'):
                    return
                elif num == 4:
                    return Resource(name=path, owner=sub.id, type='user_file'), True
                else:
                    print("You lack privileges to create that resource.")
            else:
                print('Invalid selection')
                return Resource(), False

        except ValueError as e:
            print(f'Error: invalid selection')
            sys.exit()
    else:
        return Resource(name=path, owner=sub.id, type='user_file'), True

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

        pwd = getpass("Password: ")
        if not authenticate_user(uname, pwd):
            print("Incorrect password.")
            continue
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

