# RAG Agents Demo Workshop

A hands-on workshop demonstrating how to build intelligent AI agents using Azure OpenAI's Assistants API, progressing from basic chat to advanced RAG with code execution capabilities.

## Overview

This workshop guides you through building three levels of AI agents:
1. Basic Chat Assistant - Simple conversational AI
2. RAG-Enhanced Assistant - AI with document knowledge using Azure's vector store
3. Advanced Agent - Combines RAG with code interpreter for data analysis

## Technologies Used

- **Azure OpenAI Service** - Core AI capabilities including:
  - Assistants API
  - Vector Store for document embeddings
  - File Search tool for RAG
  - Code Interpreter
- **Streamlit** - Web interface for agent interaction
- **Python** - Core programming language

## Workshop Steps

1. Set up environment:
   - Configure `.env` file (leave `ASSISTANT_ID` and `VECTOR_STORE_ID` empty)
   - Review assistant configuration in `client/azure_client.py`

2. Launch the agent:
   ```bash
   streamlit run ./azure_ai_agent/app.py
   ```

3. Progressive Enhancement Labs:
   - Lab 1: Basic assistant with customizable prompting parameters
   - Lab 2: Enable RAG capabilities using Azure's vector store and file search
   - Lab 3: Add code interpreter for data analysis and visualization

## Repository Structure

- `/azure_ai_agent` - Main application code
- `/data` - Sample documents for RAG functionality (PDF files)
- `/client` - Azure OpenAI client configuration
- `/utils` - Chat interface utilities

## Contributors

- [Jody Boelen](jodyboelen@microsoft.com)
- [Shenglin Xu ](shenglinxu@microsoft.com)

## License

This project is licensed under MIT License.