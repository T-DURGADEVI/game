from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room
import random
import threading

app = Flask(__name__)
socketio = SocketIO(app)

players = {}  # name -> sid
character_map = {}
scores = {}
game_started = False
guess_made = False
rama_name = ""
sita_name = ""
timer_thread = None

character_priority = {
    "Hanuman": 900,
    "Lakshmana": 800,
    "Ravana": 700,
    "Bharata": 600,
    "Shatrughna": 500,
    "Vali": 400,
    "Sugriva": 300
}

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('join')
def handle_join(data):
    global game_started
    name = data['name']
    if game_started or name in players:
        return

    players[name] = request.sid
    scores[name] = 0
    emit('update_players', list(players.keys()), broadcast=True)

    if len(players) >= 3 and not game_started:
        start_game()

def start_game():
    global character_map, game_started, rama_name, sita_name, timer_thread
    game_started = True

    player_names = list(players.keys())
    random.shuffle(player_names)

    # Assign Rama and Sita first
    rama_name = player_names[0]
    sita_name = player_names[1]
    character_map[rama_name] = "Rama"
    character_map[sita_name] = "Sita"

    # Assign remaining characters randomly
    remaining_chars = list(character_priority.keys())
    for i in range(2, len(player_names)):
        character_map[player_names[i]] = remaining_chars.pop(0)

    for name, sid in players.items():
        emit('your_character', {'character': character_map[name]}, room=sid)

    emit('start_timer', {}, broadcast=True)
    timer_thread = threading.Thread(target=timer_function)
    timer_thread.start()

def timer_function():
    global guess_made
    socketio.sleep(180)
    if not guess_made:
        end_game(None)  # time up

@socketio.on('send_message')
def handle_message(data):
    sender = get_name_by_sid(request.sid)
    emit('receive_message', {'name': sender, 'message': data['message']}, broadcast=True)

@socketio.on('final_guess')
def handle_guess(data):
    global guess_made
    guess_made = True
    guesser = get_name_by_sid(request.sid)
    guessed_name = data['guess']
    end_game(guessed_name)

def end_game(guessed_name):
    global scores

    # Rama guessing Sita
    if guessed_name == sita_name and rama_name in scores:
        scores[rama_name] += 1000
    elif rama_name in scores:
        scores[sita_name] += 1000

    # Other characters get based on their priority
    for name in players:
        if name not in [rama_name, sita_name]:
            char = character_map.get(name)
            scores[name] += character_priority.get(char, 0)

    emit('game_result', {
        'character_map': character_map,
        'scores': scores,
        'guessed_name': guessed_name,
        'rama': rama_name,
        'sita': sita_name
    }, broadcast=True)

def get_name_by_sid(sid):
    for name, s in players.items():
        if s == sid:
            return name
    return ""

if __name__ == '__main__':
    socketio.run(app, debug=True)
