from os import path
import sys, json, getpass, uuid, hashlib
from Crypto.Cipher import AES
import pickle

class AuthenticateUser():
    def __init__(self, user):
        self.user = user

    def hash_password(self, password):
        # uuid is used to generate a random number
        salt = uuid.uuid4().hex
        return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt

    def check_password(self, hashed_password, user_password):
        password, salt = hashed_password.split(':')
        return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()

    def add_user(self):
        while True:
            password1 = getpass.getpass(prompt='Enter password: ')
            if not password1 or not len(password1):
                print('Invalid password')
                continue
            password2 = getpass.getpass(prompt='Verify password: ')
            if password1 == password2:
                break
            else:
                print('Passwords do not match. Try again')
        self.user['password'] = self.hash_password(password1)
        self.user['saved_passwords'] = {}

    def login_user(self):
        with open('pwds', 'rb') as pwds_file:
            file_data = pickle.load(pwds_file)
            hashed_password = file_data[self.user['uname']]['password']
            while True:
                password = getpass.getpass(prompt='Enter password: ')
                if not password or not len(password):
                    print('Invalid password')
                    continue
                if self.check_password(hashed_password, password):
                    break
                else:
                    print('Wrong password. Try again')

    def authenticate_user(self):
        print("{}\nWelcome to password manager.\nLogin to continue\n{}".format('*'*30, '*'*30))
        master_uname = input('Username: ')
        file_data = {}
        with open('pwds', 'rb') as pwds_file:
            file_data = pickle.load(pwds_file)

        self.user['uname'] = master_uname
        if master_uname not in file_data:
            print('You seem to be a new user. Create an account first to proceed.')
            self.add_user()
            file_data[master_uname] = self.user
            with open('pwds', 'wb') as fp:
                fp.seek(0)
                fp.truncate(0)
                pickle.dump(file_data, fp)
        else:
            self.login_user()
            self.user['password'] = file_data[master_uname]['password']
            self.user['saved_passwords'] = file_data[master_uname]['saved_passwords']
