import os
import sys
import getpass
import argparse
from parser import parse
from cryptography.fernet import Fernet


parser = argparse.ArgumentParser(description='Automatically fetch deadlines from LMS')
parser.add_argument('--user', type=str, help='set username for future i.e --user=abc.bscs18seecs')
parser.add_argument('--pwd', type=str, help='set password for future i.e --pwd=XXXXX')
args = parser.parse_args()

user = None
pwd = None

if args.user and args.pwd:
    key = Fernet.generate_key()
    with open(".key", "wb") as key_file:
        key_file.write(key)

    fer = Fernet(key)

    with open(".config", "w") as f:
        f.write(args.user + "\n")

    with open(".pass", "wb") as pass_file:
        pass_file.write(fer.encrypt(args.pwd.encode()))

    user = args.user
    pwd = args.pwd

elif os.path.isfile(".config") and os.path.isfile(".key") and os.path.isfile(".pass"):
    with open(".key", "rb") as key_file:
        key = key_file.read()

    fer = Fernet(key)

    with open(".config", "r") as f:
        content = f.readlines()
        user = content[0]

    with open(".pass", "rb") as pass_file: 
        pwd = fer.decrypt(pass_file.read())

if user is None and pwd is None:
    if sys.stdin.isatty():
        print("Enter credentials")
        user = input("Username: ")
        pwd = getpass.getpass("Password: ")
    else:
        print("Please make sure you are using a terminal")
        sys.exit(0)

parse(user, pwd)