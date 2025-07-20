const socket = io();
let username = "";
let roomCode = "";

function createRoom() {
  username = document.getElementById("name").value;
  socket.emit("create_room", { username });
}

function joinRoom() {
  username = document.getElementById("name").value;
  roomCode = document.getElementById("room").value;
  socket.emit("join_room", { username, room: roomCode });
}

function sendMessage() {
  const msg = document.getElementById("msg").value;
  socket.emit("send_chat", { room: roomCode, username, message: msg });
}

function submitGuess() {
  const guess = document.getElementById("guessPlayer").value;
  socket.emit("submit_guess", { room: roomCode, guessed_player: guess });
}

socket.on("room_created", (data) => {
  roomCode = data.room;
  document.getElementById("players").innerText = "Room Code: " + roomCode + "\nPlayers: " + data.players.join(", ");
});

socket.on("player_joined", (data) => {
  document.getElementById("players").innerText = "Players: " + data.players.join(", ");
});

socket.on("role_assigned", (data) => {
  alert("Your role: " + data.role);
  document.getElementById("chat").style.display = "block";
  if (data.is_rama) {
    document.getElementById("guess").style.display = "block";
  }
});

socket.on("receive_chat", (data) => {
  const msgDiv = document.createElement("div");
  msgDiv.innerText = `${data.username}: ${data.message}`;
  document.getElementById("messages").appendChild(msgDiv);
});

socket.on("reveal_roles", (data) => {
  alert("Game Over!\n\nRoles:\n" + JSON.stringify(data.roles, null, 2) + "\n\nScores:\n" + JSON.stringify(data.scores, null, 2));
});
