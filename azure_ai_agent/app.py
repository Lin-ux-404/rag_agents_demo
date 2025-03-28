import streamlit as st
from client.azure_client import get_project_client
from utils.tools import initialize_tools
from utils.chat_utils import display_chat_messages, handle_user_input, reset_session_state
from configs.agent_config import AGENT_INSTRUCTIONS, AGENT_NAME
import os
from dotenv import load_dotenv

load_dotenv()

for key in ['agent_id', 'thread_id', 'messages', 'file_id', 'vector_store_id']:
    if key not in st.session_state:
        st.session_state[key] = [] if key == 'messages' else None

st.title("Employee Information Assistant")


project_client = get_project_client()

if not st.session_state.agent_id or not st.session_state.thread_id:
    with project_client:
        toolset, file, vector_store = initialize_tools(project_client)
        agent = project_client.agents.create_agent(
            model=os.getenv("AZURE_AI_AGENT_MODEL_DEPLOYMENT_NAME"),
            name=AGENT_NAME,
            instructions=AGENT_INSTRUCTIONS,
            toolset=toolset,
        )
        st.session_state.agent_id = agent.id
        st.session_state.file_id = file.id
        st.session_state.vector_store_id = vector_store.id
        thread = project_client.agents.create_thread()
        st.session_state.thread_id = thread.id

# Display chat and input
display_chat_messages()

if prompt := st.chat_input("Ask about employee information..."):
    handle_user_input(prompt, project_client)

if st.button("End Chat"):
    reset_session_state(project_client)
    st.success("Chat ended and agent deleted")
