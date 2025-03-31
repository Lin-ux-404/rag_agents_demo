import streamlit as st
import configs.agent_config as agent_config
from client.azure_client import create_or_update_vector_store, get_assistant
from utils.chat_utils import display_chat_messages, handle_user_input, reset_session_state

client, assistant = get_assistant()
create_or_update_vector_store(assistant.id)

for key in ['assistant', 'thread', 'messages']:
    if key not in st.session_state:
        st.session_state[key] = [] if key == 'messages' else None

st.title(agent_config.AGENT_NAME[0])
st.session_state['assistant'] = assistant

display_chat_messages()

if prompt := st.chat_input("Ask a question"):
    handle_user_input(prompt, client, assistant)

if st.button("End Chat"):
    reset_session_state(client)
    st.success("Chat ended and agent deleted")