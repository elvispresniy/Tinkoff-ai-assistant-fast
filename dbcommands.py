import json

from config import DATABASE_PATH

def get_chat_history():
    with open(DATABASE_PATH, "r") as file:
        db = json.load(file)

    return db

def load_chat_history(user_id):
    db = get_chat_history()

    chat_history = db[str(user_id)]

    return chat_history

def dump_chat_history(user_id, chat_history):
    db = get_chat_history()

    db[str(user_id)] = chat_history

    with open(DATABASE_PATH, "w") as file:
        json.dump(db, file)