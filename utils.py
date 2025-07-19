import random, string, os, json
import time

ROOMS_DIR = "rooms"

def generate_room_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

def create_room(host_name):
    code = generate_room_code()
    while os.path.exists(f"{ROOMS_DIR}/room_{code}.json"):
        code = generate_room_code()
    room_data = {
        "host": host_name,
        "players": {host_name: None},
        "roles": {},
        "started": False,
        "messages": [],
        "start_time": None
    }
    with open(f"{ROOMS_DIR}/room_{code}.json", "w") as f:
        json.dump(room_data, f)
    return code

def load_room(code):
    path = f"{ROOMS_DIR}/room_{code}.json"
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return None

def save_room(code, data):
    with open(f"{ROOMS_DIR}/room_{code}.json", "w") as f:
        json.dump(data, f)

def assign_roles(players):
    roles = ["Rama", "Ravana", "Sita", "Hanuman"]
    selected = random.sample(players, min(len(players), len(roles)))
    role_map = {p: r for p, r in zip(selected, roles)}
    for p in players:
        if p not in role_map:
            role_map[p] = "Commoner"
    return role_map
