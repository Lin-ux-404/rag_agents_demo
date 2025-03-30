from openai import AzureOpenAI
import os
from dotenv import load_dotenv
import configs.agent_config as agent_config
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
    Creates an assistant with file search capabilities using Azure OpenAI.
    The  API version we use here is outdated and the file search tool 
    differs from the MSLearn documentation.
    
    refrences:
    https://platform.openai.com/docs/guides/retrieval#quickstart
    https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/file-search?tabs=python
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
        name=agent_config.AGENT_NAME,
        instructions=agent_config.AGENT_INSTRUCTIONS,
        model="gpt-4o",  # Using specific model name
        tools=[{"type": "file_search"}, {"type": "code_interpreter"}],
        temperature=agent_config.TEMPERATURE,
        top_p=agent_config.TOP_P,
        max_tokens=agent_config.MAX_TOKENS,
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
