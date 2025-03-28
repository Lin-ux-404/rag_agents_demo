from openai import AzureOpenAI
import os
from dotenv import load_dotenv

load_dotenv()


def get_client():
    client = AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version="2024-05-01-preview",  # Updated to latest preview version
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
    )
    return client


def get_assistant():
    """
    Creates an assistant with file search capabilities using Azure OpenAI
    refrences:
    https://platform.openai.com/docs/guides/retrieval#quickstart

    """
    client = get_client()
    
    # Create vector store for employee documents
    vector_store = client.vector_stores.create(
        name="Employee Documents"
    )
    
    # Get all files from data directory
    data_dir = "./data"
    file_paths = [
        os.path.join(data_dir, f)
        for f in os.listdir(data_dir)
        if f.endswith(('.pdf'))  # Added more supported file types
    ]
    
    # Ready the files for upload
    file_streams = [open(path, "rb") for path in file_paths]
    
    # Upload files and poll for completion
    file_batch = client.vector_stores.file_batches.upload_and_poll(
        vector_store_id=vector_store.id,
        files=file_streams
    )
    
    print(f"Upload status: {file_batch.status}")
    print(f"File counts: {file_batch.file_counts}")
    
    # Create assistant with file search capability
    assistant = client.beta.assistants.create(
        name="Employee Information Assistant",
        instructions="You are an expert assistant. Use the provided documents to answer questions about employee information.",
        model="gpt-4o",  # Using specific model name
        tools=[{"type": "file_search"}, {"type": "code_interpreter"}]
    )
    
    # Update assistant with vector store access
    assistant = client.beta.assistants.update(
        assistant_id=assistant.id,
        tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}}
    )
    
    # Close file streams
    for file in file_streams:
        file.close()
    
    return client, assistant
