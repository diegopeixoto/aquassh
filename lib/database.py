import json
import os


def load_db():
    db_path = os.path.expanduser("~/.dotfiles/sshtool-db.json")
    if not os.path.exists(db_path):
        return None
    with open(db_path, "r") as file:
        return json.load(file)


def save_db(db):
    with open(os.path.expanduser("~/.dotfiles/sshtool-db.json"), "w") as file:
        json.dump(db, file, indent=4)
