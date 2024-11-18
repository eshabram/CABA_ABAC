import hashlib
import os
import sqlite3
from getpass import getpass
conn=sqlite3.connect('attributes.db')
cur=conn.cursor()

def check_hashed_password(password,salt):
    hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return hashed_password

def hashpassword(password):
    # Hashing using SHA-256
    salt = os.urandom(32)
    hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return hashed_password,salt

def user_exists(user):
        cur.execute('''SELECT uid FROM Passwords WHERE uid = ?''', (user,))
        username=cur.fetchone()
        if username:
            return True
        return False

def authenticate_user(username, password):
    cur. execute('''SELECT uid,salted_hash,salt from Passwords WHERE uid=?''',(username,))
    result= cur.fetchone()
    if result:
        uid,salted_hash,salt = result
        if salted_hash == check_hashed_password(password,salt):
           print("Authentication successful! Welcome")
           return True
        else:
            print("Password incorrect")
            return False



def login():
    uname = input("Enter username: ")
    if not user_exists(uname):
        print("User does not exist.")
        return

    pwd = getpass("Password: ")
    if not authenticate_user(uname, pwd):
        print("Incorrect password.")
        return
    print("Login successful.")




def register():

  uname = input("Enter your username")

  value = user_exists(uname)
     
  if value == True:
        print("Username already exists")
        return
     
      #setting the rules of the password

  PUNCTUATIONS = "@#$%&"

  DEFAULT_PASSWORD_LENGTH = 12

  INVALID_LENGTH_MESSAGE = f'''
     Password length must be between 12 and 16. 
     '''

  passwd = input("Enter a password. \n 1. Password must be between 12 to 16 characters. \n 2.Password must contain special characters: @#$%&.\n ") # Create a condition so they can't use their name or school name in the password.

  if len(passwd)<12 or len(passwd)> 16:
        print(INVALID_LENGTH_MESSAGE)
        return
    
  hpwd,salt = hashpassword(passwd)
  cur.execute('''INSERT into Passwords(uid,salted_hash,salt)
              VALUES(?,?,?)''',
              (uname, hpwd, salt))
  conn.commit()

    



    

