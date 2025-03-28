import streamlit as st
from dotenv import load_dotenv

from client.azure_client import get_assistant
from utils.chat_utils import display_chat_messages, handle_user_input, reset_session_state

load_dotenv()

client, assistant = get_assistant()

for key in ['assistant', 'thread_id', 'messages', 'file_id', 'vector_store_id']:
    if key not in st.session_state:
        st.session_state[key] = [] if key == 'messages' else None

st.title("Employee Information Assistant")
st.session_state['assistant'] = assistant

display_chat_messages()

if prompt := st.chat_input("Ask about employee information..."):
    handle_user_input(prompt, client, assistant)

if st.button("End Chat"):
    reset_session_state(client)
    st.success("Chat ended and agent deleted")