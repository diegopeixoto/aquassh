import os
import subprocess
import json
from lib.database import save_db


def initialize_db():
    print("Database not found. Initializing setup wizard...")
    print("creating database in ~/.dotfiles/sshtool-db.json")
    db_dir = os.path.expanduser("~/.dotfiles")
    os.makedirs(db_dir, exist_ok=True)
    host = input("Enter host address: ")
    host_name = input("Enter host name: ")
    user = input("Enter user: ")
    key_dir = input(
        f"Enter keys directory [{os.path.expanduser('~/.keys')}]: ") or os.path.expanduser("~/.keys")
    os.makedirs(key_dir, exist_ok=True)
    key = input("Enter key: ")
    db = {
        "last_connected_host": "",
        "key_path": key_dir,
        "hosts": {
            host: {
                "name": host_name,
                "users": [user],
                "key": key
            }
        },
        "users": [user],
        "keys": [key]
    }
    db_path = os.path.join(db_dir, "sshtool-db.json")
    with open(db_path, "w") as file:
        json.dump(db, file, indent=4)
    print(f"Database initialized at {db_path}")
    return db


def add_host(db):
    host = input("Enter host address: ")
    host_name = input("Enter host name: ")
    print("Existing users:")
    for i, user in enumerate(db['users'], 1):
        print(f"{i}. {user}")
    user_index = input(
        "Enter user index (comma separated, or 'n' to add new user): ")
    if user_index.lower() == 'n':
        new_user = input("Enter new user: ")
        db['users'].append(new_user)
        save_db(db)
        users = [new_user]
    else:
        user_index = map(int, user_index.split(','))
        users = [db['users'][index - 1] for index in user_index]

    key_index = input(
        "Enter credential key index (comma separated, or 'n' to add new credential key):")
    if key_index.lower() == 'n':
        new_key = input("Enter new key credential: ")
        db['keys'].append(new_key)
        save_db(db)
        keys = [new_key]
    else:
        key_index = map(int, key_index.split(','))
        keys = [db['keys'][index - 1] for index in key_index]
    db['hosts'][host] = {"name": host_name, "users": users, "key": keys}
    save_db(db)


def add_user(db):
    user = input("Enter user: ")
    db['users'].append(user)
    save_db(db)


def add_key(db):
    key = input("Enter key name: ")
    db['keys'].append(key)
    save_db(db)


def remove_host(db):
    print("\n".join(f"{i}. {host}" for i, host in enumerate(db['hosts'])))
    choice = input("Choose host to remove: ")
    if choice.isdigit() and int(choice) in range(len(db['hosts'])):
        host_to_remove = list(db['hosts'].keys())[int(choice)]
        del db['hosts'][host_to_remove]
        save_db(db)
        print(f"Host {host_to_remove} removed successfully.")
    else:
        print("Invalid choice, please try again.")


def remove_user(db):
    print("\n".join(f"{i}. {user}" for i, user in enumerate(db['users'])))
    choice = input("Choose user to remove: ")
    if choice.isdigit() and int(choice) in range(len(db['users'])):
        user_to_remove = db['users'][int(choice)]
        db['users'].remove(user_to_remove)
        save_db(db)
        print(f"User {user_to_remove} removed successfully.")
    else:
        print("Invalid choice, please try again.")


def remove_key(db):
    print("\n".join(f"{i}. {key}" for i, key in enumerate(db['keys'])))
    choice = input("Choose key to remove: ")
    if choice.isdigit() and int(choice) in range(len(db['keys'])):
        key_to_remove = db['keys'][int(choice)]
        db['keys'].remove(key_to_remove)
        save_db(db)
        print(f"Key {key_to_remove} removed successfully.")
    else:
        print("Invalid choice, please try again.")


def nuke_db(db):
    confirmation = input(
        "Are you sure you want to delete the database? (yes/no): ")
    if confirmation.lower() == 'yes':
        db_path = os.path.expanduser("~/.dotfiles/sshtool-db.json")
        os.remove(db_path)
        print("Database deleted successfully.")
        exit()  # Exit the script as the database is deleted
    else:
        print("Operation cancelled.")


def connect_to_host(db):
    host_keys = list(db['hosts'].keys())
    default_host_index = host_keys.index(
        db['last_connected_host']) if db['last_connected_host'] in host_keys else 0
    print("\n".join(
        f"{i}. {db['hosts'][host]['name']}" for i, host in enumerate(host_keys)))
    choice = input(f"Choose host [{default_host_index}]: ")
    choice = int(choice) if choice else default_host_index
    host = host_keys[choice]
    db['last_connected_host'] = host  # Update the last connected host
    save_db(db)  # Save the database
    print("\n".join(f"{i}. {user}" for i,
          user in enumerate(db['hosts'][host]['users'])))
    user_choice = input("Choose user [0]: ")
    user_choice = int(user_choice) if user_choice else 0
    user = db['hosts'][host]['users'][user_choice]
    key = db['hosts'][host]['key']
    command = f"ssh -i {db['key_path']}/{key} {user}@{host}"
    subprocess.run(command, shell=True)
