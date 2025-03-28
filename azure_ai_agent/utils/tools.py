import os
from azure.ai.projects.models import CodeInterpreterTool, FileSearchTool, ToolSet, OpenAIFile, VectorStore

DATA_DIR = "../data"

def initialize_tools(project_client):
    pdf_files = [
        os.path.join(DATA_DIR, f)
        for f in os.listdir(DATA_DIR)
        if f.endswith(".pdf")
    ]

    if not pdf_files:
        raise FileNotFoundError("No PDF files found in the data directory")

    files = [
        project_client.agents.upload_file_and_poll(file_path=path, purpose="assistants")
        for path in pdf_files
    ]

    vector_store = project_client.agents.create_vector_store_and_poll(
        file_ids=[f.id for f in files],
        name="company_docs_vectorstore"
    )

    toolset = ToolSet()
    toolset.add(FileSearchTool(vector_store_ids=[vector_store.id]))
    toolset.add(CodeInterpreterTool())

    return toolset, files[0], vector_store
