import os, hashlib, sqlite3, sys, base64, platform, subprocess
from db.db_interface import subject_row, add_password
from utils.entities import RESOURCE_TYPES
from getpass import getpass

conn=sqlite3.connect('db/attributes.db')
cur=conn.cursor()

def set_metadata(path, identifier):
    try:
        if platform.system() == "Darwin":  # macOS
            subprocess.run(["xattr", "-w", 'id', identifier, path], check=True)
        else:  # Linux
            subprocess.run(["setfattr", "-n", 'id', "-v", identifier, path], check=True)
        print(f"Successfully set id to {identifier} on {path}")
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
    
def select_file_type(sub):
    # TODO: we pass in subject so that we can run checks on what kinds of resources they can create
    print(f"Select resource type to create:")
    for i, type in enumerate(RESOURCE_TYPES):
        print(f'{i}. {type}')
    try:
        num = int(input('> '))
        print(num)
        sys.exit()
    except ValueError as e:
        print(f'Error: invalid selection')
        sys.exit()

def create_file(path, sub):
    if not os.path.exists(path):
        file_type = select_file_type(sub)
        try:
            with open(path, 'w') as file:
                file.write("")
            set_metadata(identifier=str(sub.id), path=path)
            return True
        except Exception as e:
            print(e)
            # print("Error: file was not created.")
            return False
    else:
        print("Error: file already exists")

def load_file(path, res):
    with open(path, 'w') as file:
        file.write(f"{res}")
    set_metadata(identifier=str(res.id), path=path)

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

