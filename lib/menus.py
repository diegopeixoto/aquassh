from lib.actions import (
    remove_host, remove_user, remove_key, nuke_db)


def create_submenu():
    print(">>> Create:")
    print("1. Add Host")
    print("2. Add User")
    print("3. Add Key")
    print("4. Back to Main Menu")
    choice = input("Choose option: ")
    return choice


def advanced_submenu(db):
    print(">>> Advanced:")
    print("1. Remove Host")
    print("2. Remove User")
    print("3. Remove Key")
    print("4. Nuke DB")
    print("5. Back to Main Menu")
    choice = input("Choose option: ")
    if choice == '1':
        remove_host(db)
    elif choice == '2':
        remove_user(db)
    elif choice == '3':
        remove_key(db)
    elif choice == '4':
        nuke_db(db)
    elif choice == '5':
        return
    else:
        print("Invalid choice, please try again.")
