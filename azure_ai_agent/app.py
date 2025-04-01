import streamlit as st
from client.azure_client import create_or_update_vector_store, get_assistant
from utils.chat_utils import display_chat_messages, handle_user_input, reset_session_state

client, assistant = get_assistant()
create_or_update_vector_store(assistant.id)

for key in ['assistant', 'thread', 'messages']:
    if key not in st.session_state:
        st.session_state[key] = [] if key == 'messages' else None

st.title("My assistant")
st.session_state['assistant'] = assistant

display_chat_messages()

if prompt := st.chat_input("Ask a question"):
    handle_user_input(prompt, client, assistant)

if st.button("End Chat"):
    reset_session_state(client)
    st.success("Chat ended and agent deleted")