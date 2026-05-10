import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

from memory_manager import (
    update_memory,
    build_context
)

load_dotenv()

# -----------------------------
# GROQ CLIENT
# -----------------------------
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# -----------------------------
# STREAMLIT PAGE
# -----------------------------
st.set_page_config(
    page_title="AI Study Assistant",
    layout="wide"
)

st.title("AI Study Assistant with Memory")

# -----------------------------
# SESSION STATE
# -----------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "recent_messages" not in st.session_state:
    st.session_state.recent_messages = []

if "summary_memory" not in st.session_state:
    st.session_state.summary_memory = ""

if "important_memories" not in st.session_state:
    st.session_state.important_memories = []

# -----------------------------
# USER INPUT
# -----------------------------
user_input = st.chat_input(
    "Ask something..."
)

# -----------------------------
# CHAT PROCESS
# -----------------------------
if user_input:

    # Build full context
    context = build_context(user_input)

    # Add latest user message
    context.append({
        "role": "user",
        "content": user_input
    })

    # LLM Response
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=context
    )

    assistant_reply = (
        response.choices[0]
        .message.content
    )

    # Update memory
    update_memory(
        user_input,
        assistant_reply
    )

    # Store chat history for UI
    st.session_state.chat_history.append(
        ("You", user_input)
    )

    st.session_state.chat_history.append(
        ("Assistant", assistant_reply)
    )

# -----------------------------
# DISPLAY CHAT
# -----------------------------
for role, message in (
    st.session_state.chat_history
):

    st.write(f"**{role}:** {message}")