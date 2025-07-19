import streamlit as st
import time
from utils import create_room, load_room, save_room, assign_roles

st.set_page_config(page_title="Ramayana Game", layout="wide")

st.title("🌟 Ramayana Secret Identity Game")

# Get user input
username = st.text_input("Enter your name:", key="username")
mode = st.radio("Choose mode:", ["Create Room", "Join Room"])

if username:
    if mode == "Create Room":
        if st.button("Create"):
            code = create_room(username)
            st.session_state.room_code = code
            st.success(f"Room created! Code: `{code}`")

    elif mode == "Join Room":
        code = st.text_input("Enter Room Code:")
        if st.button("Join"):
            room = load_room(code)
            if room:
                room["players"][username] = None
                save_room(code, room)
                st.session_state.room_code = code
                st.success(f"Joined room `{code}` successfully.")
            else:
                st.error("Room not found.")

# Once in a room
if "room_code" in st.session_state:
    code = st.session_state.room_code
    room = load_room(code)

    st.subheader(f"Room: {code}")
    st.write("Players:", ", ".join(room["players"].keys()))

    if username == room["host"] and not room["started"]:
        if st.button("Start Game"):
            room["roles"] = assign_roles(list(room["players"].keys()))
            room["started"] = True
            room["start_time"] = time.time()
            save_room(code, room)
            st.rerun()

    if room["started"]:
        role = room["roles"][username]
        st.info(f"Your role: **{role}**")

        if role == "Rama":
            st.warning("You are Rama. Others may try to deceive you!")
        else:
            st.success("You know your role. Keep it secret!")

        # Timer
        elapsed = time.time() - room["start_time"]
        remaining = int(120 - elapsed)
        if remaining > 0:
            st.metric("⏰ Time Remaining", f"{remaining}s")
        else:
            st.error("⏱️ Time’s up! Rama has lost.")
            st.stop()

        # Chat
        st.markdown("### 💬 Chat")
        for msg in room["messages"]:
            st.write(f"**{msg['sender']}**: {msg['text']}")
        
        chat_input = st.text_input("Send a message:", key="chat")
        if st.button("Send"):
            room["messages"].append({"sender": username, "text": chat_input})
            save_room(code, room)
            st.rerun()

        # Rama can guess
        if role == "Rama":
            guess = st.selectbox("Who do you think is Ravana?", list(room["players"].keys()))
            if st.button("Submit Guess"):
                actual = [p for p, r in room["roles"].items() if r == "Ravana"][0]
                if guess == actual:
                    st.success("🎉 Correct! You found Ravana!")
                else:
                    st.error(f"❌ Wrong! Ravana was {actual}.")
