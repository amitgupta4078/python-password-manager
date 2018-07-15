from os import path
import sys, json, getpass, uuid, hashlib
from Crypto.Cipher import AES

def encrypt_password(password):
    obj = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
    return obj.encrypt(password)

def decrypt_password(encrypted_password):
    obj2 = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
    return obj2.decrypt(ciphertext)

def hash_password(password):
    # uuid is used to generate a random number
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt

def check_password(hashed_password, user_password):
    password, salt = hashed_password.split(':')
    return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()

def get_master_username():
    return input('Username: ')

def add_user(user):
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
    user['password'] = hash_password(password1)
    user['saved_passwords'] = {}

def login_user(user):
    with open('pwds', 'r') as pwds_file:
        file_data = json.load(pwds_file)
        hashed_password = file_data[user['uname']]['password']
        while True:
            password = getpass.getpass(prompt='Enter password: ')
            if not password or not len(password):
                print('Invalid password')
                continue
            if check_password(hashed_password, password):
                break
            else:
                print('Wrong password. Try again')

def authenticate_user(user):
    master_uname = get_master_username()
    with open('pwds', 'r+') as pwds_file:
        file_data = json.load(pwds_file)
        user['uname'] = master_uname
        if master_uname not in file_data:
            print('You seem to be a new user. Create an account first to proceed.')
            add_user(user)
            file_data[master_uname] = user
            pwds_file.seek(0)
            pwds_file.truncate(0)
            json.dump(file_data, pwds_file)
        else:
            login_user(user)
            user['password'] = file_data[master_uname]['password']
            user['saved_passwords'] = file_data[master_uname]['saved_passwords']

def show_options(user):
    while True:
        print('Select an option below:\n1. Retrieve a password\n2. Add a new password\n3. Quit the application')
        option = input('> ')
        if option in ('1', '2', '3'):
            break;
        else:
            print('Invalid selection. Try again.')
    
    return option

def retrieve_password(user):
    try:
        with open('pwds', 'r') as pwds_file:
            portal = input('Enter the application name: ')
            file_data = json.load(pwds_file)
            if portal in file_data[user['uname']]['saved_passwords']:
                print('test: ', file_data[user['uname']]['saved_passwords'].get(portal, None))
                portal_password = file_data[user['uname']]['saved_passwords'].get(portal, None)
                cooked_password = decrypt_password(portal_password)
                print('Password for {} is {}\n'.format(portal, portal_password))
            else:
                print('No entry found corresponding to {}. Do you want to store it now? (y/n)'.format(portal))
                choice = input('> ')
                if choice in ('Y', 'y', 'yes', 'YES'):
                    store_password(user)
    except Exception as exception:
        print(exception)

def store_password(user):
    try:
        with open('pwds', 'r+') as pwds_file:
            portal = input('Enter the application name: ')
            file_data = json.load(pwds_file)
            if portal not in file_data[user['uname']]['saved_passwords']:
                while True:
                    portal_password1 = getpass.getpass(prompt='Enter password: ')
                    if portal_password1 and len(portal_password1):
                        portal_password2 = getpass.getpass(prompt='Confirm password: ')
                        if portal_password1 == portal_password2:
                            break
                    else:
                        print('Invalid password. Try again')
                file_data[user['uname']]['saved_passwords'][portal] = encrypt_password(portal_password1)
                pwds_file.seek(0)
                pwds_file.truncate(0)
                json.dump(file_data, pwds_file)
            else:
                print('Entry already exists for {}').format(portal)
                return
    except Exception as exception:
        print(exception)


def handle_selected_option(option, user):
    if option == '1':
        retrieve_password(user)
    elif option == '2':
        store_password(user)
    elif option == '3':
        sys.exit(0)
    else:
        return

def main():
    try:
        # Check if master passwords file exists; else create
        if not path.exists('pwds'):
            print('File does not exist')
            with open('pwds', 'w') as fp:
                json.dump({}, fp)
    except Exception as exception:
        print('Exception occurred while bootstrapping the script: ', exception)        

    user = {}
    # Greet user and do master login
    print("{}\nWelcome to password manager.\nLogin to continue\n{}".format('*'*30, '*'*30))
    authenticate_user(user)
    print("\n{}\nLogin successful.\nHello {}\n{}\n".format('-'*30, user['uname'], '-'*30))
    while True:
        option = show_options(user)
        handle_selected_option(option, user)

if __name__ == '__main__':
    main()
