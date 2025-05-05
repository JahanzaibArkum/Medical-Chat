import streamlit as st
import requests
import os

try:
    API_KEY = st.secrets["MISTRAL_API_KEY"]
except KeyError:
    st.error("❌ MISTRAL_API_KEY not found in Streamlit secrets. Please add it in the cloud secrets tab.")
    st.stop()


MISTRAL_URL = "https://api.mistral.ai/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# --- Mistral API Call ---
def ask_mistral(messages):
    data = {
        "model": "mistral-medium",
        "messages": messages,
        "temperature": 0.9,
        "max_tokens": 1500
    }
    response = requests.post(MISTRAL_URL, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code} - {response.text}"

# --- Streamlit App Setup ---
st.set_page_config(page_title="Medical Chatbot", page_icon="🩺", layout="wide")

# --- Custom CSS for Dark Theme UI ---
st.markdown("""
    <style>
        /* Global Styling */
        body {
            background-color: #121212;
            color: #e5e5e5;
            font-family: 'Roboto', sans-serif;
        }
        h1 {
            font-family: 'Roboto', sans-serif;
            color: #e5e5e5;
            font-size: 36px;
            text-align: center;
            margin-top: 20px;
        }
        h2 {
            font-size: 24px;
            color: #e5e5e5;
            font-weight: bold;
        }
        .stTextInput, .stTextArea {
            border-radius: 10px;
            padding: 12px;
            font-size: 18px;
            background-color: #333;
            color: #fff;
            border: 1px solid #444;
        }
        .stButton button {
            background-color: #4CAF50;
            color: white;
            font-size: 18px;
            padding: 12px 24px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            transition: background-color 0.3s ease;
        }
        .stButton button:hover {
            background-color: #45a049;
        }

        /* Chat Styling */
        .chat-message {
            font-size: 18px;
            padding: 15px;
            border-radius: 15px;
            margin-bottom: 16px;
            max-width: 80%;
            word-wrap: break-word;
            transition: all 0.3s ease;
        }
        .user-message {
            background-color: #00796b;
            color: #e5e5e5;
            text-align: left;
            margin-right: auto;
            border-radius: 15px 15px 0 15px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
        }
        .assistant-message {
            background-color: #333;
            color: #e5e5e5;
            text-align: left;
            margin-left: auto;
            border-radius: 15px 15px 15px 0;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
        }

        /* Sidebar Styling */
        .sidebar {
            background-color: #2c2c2c;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        }
        .sidebar h2 {
            font-size: 22px;
            color: #e5e5e5;
            font-weight: bold;
        }
        .sidebar .stMarkdown {
            font-size: 14px;
            color: #b5b5b5;
        }

        /* Smooth Transition for Messages */
        .chat-message {
            animation: fadeIn 0.6s ease-out;
        }

        @keyframes fadeIn {
            0% { opacity: 0; transform: translateY(20px); }
            100% { opacity: 1; transform: translateY(0); }
        }
    </style>
""", unsafe_allow_html=True)

# --- Streamlit Title and Description ---
st.title("🩺 Medical Chatbot by Jahanzaib")
st.markdown(
    "_Ask only medical-related questions. Other topics will be politely declined._\n"
    "This chatbot helps you with medical-related inquiries, such as symptoms, treatments, and medications."
)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "You are a strict medical assistant. You are only allowed to respond to medical questions "
                "(e.g., about symptoms, treatments, diseases, medications, body systems, or diagnoses). "
                "If the user's question is not clearly and explicitly medical, reply only with: "
                "'Sorry, I can only assist with medical-related questions.' "
                "Do not explain or add any extra information for unrelated topics."
            )
        }
    ]
     
# --- Sidebar: Conversation History (Thread View) ---
with st.sidebar:
    st.header("🧵 Thread History")
    for i, msg in enumerate(st.session_state.messages[1:]):  # Skip system message
        role = msg["role"].capitalize()
        st.markdown(f"**{role}:** {msg['content'][:150]}{'...' if len(msg['content']) > 150 else ''}")
        st.divider()

# --- Main Chat Area: Display conversation ---
for msg in st.session_state.messages[1:]:  # Skip system message
    with st.chat_message(msg["role"]):
        # Add custom classes for styling
        message_class = "user-message" if msg["role"] == "user" else "assistant-message"
        st.markdown(f'<div class="chat-message {message_class}">{msg["content"]}</div>', unsafe_allow_html=True)

# --- Chat Input ---
if prompt := st.chat_input("Enter your medical question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(f'<div class="chat-message user-message">{prompt}</div>', unsafe_allow_html=True)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            reply = ask_mistral(st.session_state.messages)
            st.markdown(f'<div class="chat-message assistant-message">{reply}</div>', unsafe_allow_html=True)
            st.session_state.messages.append({"role": "assistant", "content": reply})
