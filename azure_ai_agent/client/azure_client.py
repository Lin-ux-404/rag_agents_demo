from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
import os
from dotenv import load_dotenv

load_dotenv()

def get_project_client():
    credential = DefaultAzureCredential(
        exclude_environment_credential=True,
        exclude_managed_identity_credential=True
    )
    return AIProjectClient.from_connection_string(credential=credential, conn_str=os.getenv("AZURE_AI_AGENT_PROJECT_CONNECTION_STRING"))
