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

1. Fork this repository and open it in GitHub Code Spaces.

2. Set up environment:
   - Configure `.env` file (leave `ASSISTANT_ID` and `VECTOR_STORE_ID` empty). You can copy and renae the `.env.sample` file for this.
   - Review assistant configuration in `azure_ai_agent/client/azure_client.py`

3. Launch the agent. To Run the agent, run the following command. This will start the app with streamlit, after which you can click on the localhost url. This should open the chat interface in your browser.
   ```bash
   streamlit run ./azure_ai_agent/app.py
   ```

4. Play with the different set-ups in `azure_ai_agent/client/azure_client.py` to change the behavior of your agent. See the section below for some ideas.

Progressive Enhancement Labs:
   - Lab 1: Basic assistant with customizable prompting parameters
   - Lab 2: Enable RAG capabilities using Azure's vector store and file search
   - Lab 3: Add code interpreter for data analysis and visualization

## Progressive agent enhancements

### 1. Customize the behavior of the agent with prompting

To start customizing the agent's behavior, you can adjust the system prompt that is passed to the agent. To do this, open the `azure_ai_agent/client/azure_client.py` file and adjust the variables at the top of the file (line 6-9). 

### 2. Enable RAG capabilities using Azure's vector store and file search

The data folder contains some sample pdfs, but the agent does not yet consider this data. To add this capability, comment out the initial client (line 25-33) in the `azure_ai_agent/client/azure_client.py` file and uncomment line 36-44 to update the agent with RAG capabilities. Notice that this adds the file search tool and grants the agent access to a vector store resource. Rerun the application and you can start asking questions about the pdf files.

### 3. Add code interpreter for data analysis and visualization

The next iteration of the agent includes code execution capabilities. Similar to step 2, uncomment the previous client in the `azure_ai_agent/client/azure_client.py` file and uncomment line 47-55. This adds the code interpreter tool. Rerun the application and you should now be able to ask the agent to generate graphs for example. As an example, you could try: `Can you group all employees by job title and plot this on a graph?`.

## Repository Structure

- `/data` - Sample documents for RAG functionality (PDF files)
- `/azure_ai_agent` - Main application code
- `/azure_ai_agent/client` -  Azure OpenAI client configuration
- `/azure_ai_agent/utils` -  Chat interface utilities


## Contributors

- [Jody Boelen](jodyboelen@microsoft.com)
- [Shenglin Xu ](shenglinxu@microsoft.com)

## License

This project is licensed under MIT License.