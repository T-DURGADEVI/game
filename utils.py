import json
import os
import random
from datetime import datetime

DATA_FILE = "rooms.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

def create_room(host):
    code = str(random.randint(1000, 9999))
    data = load_data()
    data[code] = {
        "host": host,
        "players": {host: None},
        "started": False,
        "roles": {},
        "messages": [],
        "start_time": None
    }
    save_data(data)
    return code

def load_room(code):
    return load_data().get(code)

def save_room(code, room):
    data = load_data()
    data[code] = room
    save_data(data)

def assign_roles(players):
    roles = ["Rama", "Sita"] + ["Vanara"] * (len(players) - 2)
    random.shuffle(roles)
    return dict(zip(players, roles))
