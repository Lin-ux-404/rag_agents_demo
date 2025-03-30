"""
Agent configuration for the Employee Information Agent.
This configuration includes the agent's name, instructions, and model parameters.
"""

AGENT_NAME = "Employee Information Assistant",
AGENT_INSTRUCTIONS = (
    "You are an expert assistant." 
    "Use the provided documents to answer questions about employee information."
)


TEMPERATURE = 0.5
TOP_P = 0.9
MAX_TOKENS = 500