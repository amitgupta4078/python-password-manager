from os import path
import sys, json, pickle
from portalauthentication import AuthenticateUser
from passwordmanager import PwdManager


def show_options():
    while True:
        print('Select an option below:\n1. Retrieve a password\n2. Add a new password\n3. Quit the application')
        option = input('> ')
        if option in ('1', '2', '3'):
            break;
        else:
            print('Invalid selection. Try again.')
    
    return option


def handle_selected_option(option, pwd_manager):
    if option == '1':
        pwd_manager.retrieve_password()
    elif option == '2':
        pwd_manager.store_password()
    elif option == '3':
        sys.exit(0)
    else:
        return


def main():
    try:
        # Check if master passwords file exists; else create
        if not path.exists('pwds') or not path.isfile('pwds'):
            print('File does not exist')
            with open('pwds', 'wb') as fp:
                pickle.dump({}, fp)
    except Exception as exception:
        print('Exception occurred while bootstrapping the script: ', exception)

    user = {}
    
    portal_authorizer = AuthenticateUser(user)
    portal_authorizer.authenticate_user()

    print("\n{}\nLogin successful.\nHello {}\n{}\n".format('-'*30, user['uname'], '-'*30))
    pwd_manager = PwdManager(user)

    while True:
        option = show_options()
        handle_selected_option(option, pwd_manager)


if __name__ == '__main__':
    main()
