from os import path
import sys, json, getpass, uuid, hashlib, pickle
from Crypto.Cipher import AES

class PwdManager():
    def __init__(self, user):
        self.user = user

    def retrieve_password(self):
        try:
            portal = input('Enter the application name: ')
            with open('pwds', 'rb') as pwds_file:
                file_data = pickle.load(pwds_file)
            if portal in file_data[self.user['uname']]['saved_passwords']:
                portal_password = file_data[self.user['uname']]['saved_passwords'].get(portal, None)
                cooked_password = self.decrypt_password(portal_password)
                print('Password for {} is {}\n'.format(portal, cooked_password))
            else:
                print('No entry found corresponding to {}. Do you want to store it now? (y/n)'.format(portal))
                choice = input('> ')
                if choice in ('Y', 'y', 'yes', 'YES'):
                    self.store_password()
        except Exception as exception:
            print(exception)

    def store_password(self):
        try:
            portal = input('Enter the application name: ')
            with open('pwds', 'rb') as pwds_file:
                file_data = pickle.load(pwds_file)
            if portal not in file_data[self.user['uname']]['saved_passwords']:
                while True:
                    portal_password1 = getpass.getpass(prompt='Enter password: ')
                    if portal_password1 and len(portal_password1):
                        portal_password2 = getpass.getpass(prompt='Confirm password: ')
                        if portal_password1 == portal_password2:
                            break
                        else:
                            print('Passwords don\'t match. Try again.')
                    else:
                        print('Invalid password. Try again')
                file_data[self.user['uname']]['saved_passwords'][portal] = self.encrypt_password(portal_password1)
                with open('pwds', 'wb') as fp:
                    fp.seek(0)
                    fp.truncate(0)
                    pickle.dump(file_data, fp)
            else:
                print('Entry already exists for {}').format(portal)
                return
        except Exception as exception:
            print(exception)


    def encrypt_password(self, password):
        obj = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
        padded_length = len(password) % 16
        password = '.' * (16 - padded_length) + password
        return obj.encrypt(password)


    def decrypt_password(self, encrypted_password):
        obj2 = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
        temp = obj2.decrypt(encrypted_password).decode().lstrip('.')
        return temp
