from openai import AzureOpenAI
import os
from dotenv import load_dotenv, set_key
load_dotenv()

agent_name = "agent"
system_prompt = "You are a friendly assistant that helps users with their questions." 
temperature = 0.5
top_p = 0.9

def get_assistant():
    """
    Creates an assistant with file search capabilities using Azure OpenAI.
    The  API version we use here is outdated and the file search tool 
    differs from the MSLearn documentation.

    refrences:
    https://platform.openai.com/docs/guides/retrieval#quickstart
    https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/file-search?tabs=python
    """
    client = get_client()
    assistant = get_or_create_assistant()

    ## 1. Basic assistant.
    client.beta.assistants.update(
        assistant.id,
        instructions=system_prompt,
        model=os.getenv("AZURE_OPENAI_MODEL_NAME"),
        temperature=temperature,
        tools=[],
        tool_resources={},
        top_p=top_p
    )

    ## 2. RAG assistant.
    # client.beta.assistants.update(
    #     assistant.id,
    #     instructions=system_prompt,
    #     model=os.getenv("AZURE_OPENAI_MODEL_NAME"),
    #     temperature=temperature,
    #     tools=[{"type": "file_search"}],
    #     tool_resources={"file_search": {"vector_store_ids": [os.environ["VECTOR_STORE_ID"]]}},
    #     top_p=top_p
    # )

    ## 3. RAG and code execution assistant.
    # client.beta.assistants.update(
    #     assistant.id,
    #     instructions=system_prompt,
    #     model=os.getenv("AZURE_OPENAI_MODEL_NAME"),
    #     temperature=temperature,
    #     tools=[{"type": "file_search"}, {"type": "code_interpreter"}],
    #     tool_resources={},
    #     top_p=top_p
    # )

    return client, assistant


def get_client():
    client = AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version="2024-05-01-preview",
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
    )
    return client


def get_or_create_assistant():
    """
    Retrieves an existing assistant or creates a new one if it doesn't exist.
    """
    client = get_client()

    assistant_id = os.getenv("ASSISTANT_ID")

    if assistant_id:
        assistant = client.beta.assistants.retrieve(
            assistant_id=assistant_id
        )

        return assistant

    else:
        assistant = client.beta.assistants.create(
            name=agent_name,
            model=os.getenv("AZURE_OPENAI_MODEL_NAME"),
            temperature=temperature,
            top_p=top_p
        )

        set_key(".env", "ASSISTANT_ID", assistant.id)
        os.environ["ASSISTANT_ID"] = assistant.id
        return assistant


def create_or_update_vector_store(assistantId):
    """
    Creates or updates a vector store for the assistant.
    """
    client = get_client()

    vector_store_id = os.getenv("VECTOR_STORE_ID")
    vector_store = None

    if vector_store_id:
        vector_store = client.vector_stores.retrieve(
            vector_store_id=vector_store_id
        )
    else:
        vector_store = client.vector_stores.create(
            name=f"vs_{assistantId}"
        )
        set_key(".env", "VECTOR_STORE_ID", vector_store.id)
        os.environ["VECTOR_STORE_ID"] = vector_store.id

    # Get all files from data directory
    data_dir = "./data"
    file_paths = [
        os.path.join(data_dir, f)
        for f in os.listdir(data_dir)
        if f.endswith(('.pdf'))  # Added more supported file types
    ]

    ## Get all files and delete them.
    for file in client.vector_stores.files.list(vector_store_id=vector_store.id):
        client.vector_stores.files.delete(
            vector_store_id=vector_store.id,
            file_id=file.id
        )

    # Ready the files for upload
    file_streams = [open(path, "rb") for path in file_paths]

    # Upload files and poll for completion
    client.vector_stores.file_batches.upload_and_poll(
        vector_store_id=vector_store.id,
        files=file_streams
    )

    # Close file streams
    for file in file_streams:
        file.close()

    return vector_store
