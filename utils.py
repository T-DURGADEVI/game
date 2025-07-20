import os
import json
import random
import string

ROOMS_DIR = "rooms"

if not os.path.exists(ROOMS_DIR):
    os.makedirs(ROOMS_DIR)

def create_room(host_name):
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    room_data = {
        "host": host_name,
        "players": {host_name: None},
        "started": False,
        "roles": {},
        "messages": [],
        "start_time": None
    }
    save_room(code, room_data)
    return code

def load_room(code):
    try:
        with open(os.path.join(ROOMS_DIR, f"{code}.json"), "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def save_room(code, data):
    with open(os.path.join(ROOMS_DIR, f"{code}.json"), "w") as f:
        json.dump(data, f)

def assign_roles(players):
    roles = ["Rama", "Sita", "Ravana"]
    others = ["Helper"] * (len(players) - 3)
    all_roles = roles + others
    random.shuffle(all_roles)
    return dict(zip(players, all_roles))
