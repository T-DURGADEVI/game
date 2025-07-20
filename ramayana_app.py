import streamlit as st
import time
from utils import create_room, load_room, save_room, assign_roles

st.set_page_config(page_title="Ramayana Game", layout="wide")
st.title("🌟 Ramayana Secret Identity Game")

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
                if username not in room["players"]:
                    room["players"][username] = None
                    save_room(code, room)
                st.session_state.room_code = code
                st.success(f"Joined room `{code}` successfully.")
            else:
                st.error("Room not found.")

if "room_code" in st.session_state:
    code = st.session_state.room_code
    room = load_room(code)

    st.subheader(f"Room Code: {code}")
    st.write("👥 Players:", ", ".join(room["players"].keys()))

    if username == room["host"] and not room["started"]:
        if len(room["players"]) < 3:
            st.warning("At least 3 players are needed to start the game.")
        else:
            if st.button("Start Game"):
                room["roles"] = assign_roles(list(room["players"].keys()))
                room["started"] = True
                room["start_time"] = time.time()
                save_room(code, room)
                st.rerun()

    if room["started"]:
        role = room["roles"].get(username)
        st.info(f"Your role: **{role}**")

        if role == "Rama":
            st.warning("🧘 You are **Rama**. Your mission is to find **Sita**.")
        elif role == "Sita":
            st.success("🧝‍♀️ You are **Sita**. Stay hidden!")
        elif role == "Ravana":
            st.error("😈 You are **Ravana**. Confuse Rama!")
        else:
            st.success("🔍 You are a helper. Play along!")

        # Timer logic
        elapsed = time.time() - room["start_time"]
        remaining = int(120 - elapsed)
        if remaining > 0:
            st.metric("⏰ Time Remaining", f"{remaining}s")
        else:
            if role == "Rama":
                st.error("⏱️ Time’s up! Rama has lost.")
            st.stop()

        # Chat Section
        st.markdown("### 💬 Chat")
        for msg in room["messages"]:
            st.write(f"**{msg['sender']}**: {msg['text']}")
        
        chat_input = st.text_input("Send a message:", key="chat")
        if st.button("Send"):
            if chat_input:
                room["messages"].append({"sender": username, "text": chat_input})
                save_room(code, room)
                st.rerun()

        # Rama guesses Sita
        if role == "Rama":
            guess = st.selectbox("Who do you think is **Sita**?", [p for p in room["players"].keys() if p != username])
            if st.button("Submit Guess"):
                actual_sita = [p for p, r in room["roles"].items() if r == "Sita"][0]
                if guess == actual_sita:
                    st.success("🎉 Correct! You found **Sita**. Rama wins!")
                else:
                    st.error(f"❌ Wrong! **Sita** was {actual_sita}. Rama loses.")
