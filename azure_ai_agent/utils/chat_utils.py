import streamlit as st
import io
from PIL import Image

def display_chat_messages():
    """Display chat messages from session state."""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "image_data" in message:
                st.image(message["image_data"])

def handle_user_input(prompt: str, project_client) -> None:
    """Handle user input and get agent response."""

    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            with project_client:
                
                message = project_client.agents.create_message(
                    thread_id=st.session_state.thread_id,
                    role="user",
                    content=prompt
                )

                # Run the agent
                run = project_client.agents.create_and_process_run(
                    thread_id=st.session_state.thread_id,
                    agent_id=st.session_state.agent_id
                )

                if run.status == "failed":
                    error_message = f"Run failed: {run.last_error}"
                    st.error(error_message)
                    st.session_state.messages.append({"role": "assistant", "content": error_message})
                else:
                    # Get messages from the thread
                    messages = project_client.agents.list_messages(thread_id=st.session_state.thread_id)
                    last_msg = messages.get_last_text_message_by_role("assistant")
                    
                    if last_msg:
                        response_text = last_msg.text.value
                        st.markdown(response_text)
                        response_dict = {"role": "assistant", "content": response_text}

                        current_run_messages = [msg for msg in messages.data if msg.run_id == run.id]
                        for message in current_run_messages:
                            if hasattr(message, 'image_contents'):
                                for image_content in message.image_contents:
                                    # Get image data directly from API and convert to bytes
                                    image_bytes = b''.join(project_client.agents.get_file_content(
                                        file_id=image_content.image_file.file_id
                                    ))
                                    
                                    image_data = Image.open(io.BytesIO(image_bytes))
                                    
                                    st.image(image_data)
                                    response_dict["image_data"] = image_data
                        
                        st.session_state.messages.append(response_dict)

def reset_session_state(project_client) -> None:
    """Reset session state and delete agent."""
    if st.session_state.agent_id:
        with project_client:
            project_client.agents.delete_agent(st.session_state.agent_id)
    
    for key in ['agent_id', 'thread_id', 'messages', 'file_id', 'vector_store_id']:
        st.session_state[key] = [] if key == 'messages' else None
