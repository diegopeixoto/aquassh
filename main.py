import os
from datetime import datetime
from lib.database import load_db
from lib.menus import create_submenu, advanced_submenu
from lib.actions import (initialize_db, add_host, add_user, add_key,
                         connect_to_host)


def print_centered(text):
    term_width = os.get_terminal_size().columns
    text_width = max(len(line) for line in text.splitlines())
    left_padding = (term_width - text_width) // 2
    print('\n'.join(line.center(term_width) for line in text.splitlines()))


def main():
    ascii_logo = """
         _     _              _
 ___ ___| |__ | |_ ___   ___ | |
/ __/ __| '_ \| __/ _ \ / _ \| |
\__ \__ \ | | | || (_) | (_) | |
|___/___/_| |_|\__\___/ \___/|_|
    """
    current_year = datetime.now().year
    copyright_text = f"(C) 2023 - {current_year} Diego Peixoto - All rights reserved. github.com/diegopeixoto"

    print_centered(ascii_logo)
    print_centered(copyright_text)
    try:
        db = load_db()
        if db is None:
            db = initialize_db()
        while True:
            print("1. Connect to Host\n2. Create\n3. Advanced\n4. Exit")
            choice = input("Choose option [1]: ") or '1'
            if choice == '1':
                connect_to_host(db)
            elif choice == '2':
                while True:
                    sub_choice = create_submenu()
                    if sub_choice == '1':
                        add_host(db)
                    elif sub_choice == '2':
                        add_user(db)
                    elif sub_choice == '3':
                        add_key(db)
                    elif sub_choice == '4':
                        break
                    else:
                        print("Invalid choice, please try again.")
            elif choice == '3':
                advanced_submenu(db)
            elif choice == '4':
                break
            else:
                print("Invalid choice, please try again.")
    except Exception as e:
        print(f"An error occurred: {e}")
        choice = input("Would you like to open an issue? (yes/no): ").lower()
        if choice == 'yes':
            print("Please visit: https://github.com/diegopeixoto/sshtool/issues")
    except KeyboardInterrupt:
        print("\nSee ya soon!")


if __name__ == "__main__":
    main()
