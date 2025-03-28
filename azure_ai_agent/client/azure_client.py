from openai import AzureOpenAI
import os
from dotenv import load_dotenv

load_dotenv()


def get_client():
    client = AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version="2024-05-01-preview",
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
    )

    

    return client


def get_assistant():
    client = get_client()
    assistant = client.beta.assistants.create(
        model="gpt-4o",
        name="Assistant798",
        instructions="",
        tools=[{"type": "code_interpreter"}],
        temperature=1,
        top_p=1
    )

    return client, assistant
