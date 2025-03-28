import os
from dotenv import load_dotenv

load_dotenv()

AGENT_NAME = "employee-info-agent"
AGENT_INSTRUCTIONS = (
    "You are a helpful agent who provides information about employees. "
    "Keep answers concise, but include as much relevant data as possible."
)
