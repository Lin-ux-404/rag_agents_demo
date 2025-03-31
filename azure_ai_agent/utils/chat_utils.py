import streamlit as st
import io
from PIL import Image
import queue
import json
from client.azure_client import get_client

tool_requests = queue.Queue()
client = get_client()

def display_chat_messages():
    """Display chat messages from session state."""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

def handle_user_input(prompt: str, client, assistant) -> None:
    """Handle user input and get agent response."""

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("Thinking..."):
        with client:
            if st.session_state['thread'] is not None:
                thread = st.session_state['thread']
            else:
                thread = client.beta.threads.create()
                st.session_state['thread'] = thread

            client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content=prompt
            )

            with client.beta.threads.runs.stream(
                thread_id=thread.id,
                assistant_id=assistant.id
            ) as stream:
                display_stream(stream)
                while not tool_requests.empty():
                    tool_outputs, thread_id, run_id = handle_requires_action(
                        tool_requests.get())
                    with client.beta.threads.runs.submit_tool_outputs_stream(
                            thread_id=thread_id,
                            run_id=run_id,
                            tool_outputs=tool_outputs
                    ) as tool_stream:
                        display_stream(tool_stream, create_context=False)


def reset_session_state(client) -> None:
    """Reset session state and delete agent."""
    client.beta.threads.delete(st.session_state['thread'].id)
    for key in ['assistant', 'thread', 'messages']:
        if key not in st.session_state:
            st.session_state[key] = [] if key == 'messages' else None


def handle_requires_action(tool_request):
    tool_outputs = []
    data = tool_request.data
    for tool in data.required_action.submit_tool_outputs.tool_calls:
        match tool.function.name:
            case _:
                ret_val = {
                    "status": "error",
                    "message": f"Function name is not recognize. Make sure you submit the request with the correct "
                    f"request structure. Fix your request and try again"
                }
                tool_outputs.append(
                    {"tool_call_id": tool.id, "output": json.dumps(ret_val)})
    return tool_outputs, data.thread_id, data.id


def data_streamer():
    content_produced = False
    for response in st.session_state.stream:
        match response.event:
            case "thread.message.delta":
                content = response.data.delta.content[0]
                match content.type:
                    case "text":
                        value = content.text.value
                        content_produced = True
                        yield value
                    case "image_file":
                        image_content = io.BytesIO(client.files.content(
                            content.image_file.file_id).read())
                        content_produced = True
                        yield Image.open(image_content)
            case "thread.run.requires_action":
                tool_requests.put(response)
                if not content_produced:
                    yield "[LLM requires a function call]"
                return
            case "thread.run.failed":
                return


def add_message_to_state_session(message):
    st.session_state.messages.append({"role": "assistant", "content": message})


def display_stream(content_stream, create_context=True):
    st.session_state.stream = content_stream
    if create_context:
        with st.chat_message("assistant"):
            response = st.write_stream(data_streamer)
    else:
        response = st.write_stream(data_streamer)
    if response is not None:
        if isinstance(response, list):
            # Multiple messages in the response
            for message in response:
                add_message_to_state_session(message)
        else:
            # Single message in response
            add_message_to_state_session(response)
