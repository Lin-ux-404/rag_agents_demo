# rag_agents_demo

1. Set .env file according to the sample. Leave `ASSISTANT_ID` and `VECTOR_STORE_ID` empty.
2. Go to client/azure_client and look at the get_assistant function.
3. run the agent by typing `streamlit run ./azure_ai_agent/app.py` in your terminal and play around with the chat.
4. Change the system_prompt, temperature and top_p parameters in the azure_client.py file and re-run the app to see how prompting changes the behavior.
5. Comment out `## 1. Basic assistant.` and uncomment `## 2. RAG assistant.`. This will add RAG capabilities to your agent. Re-run and try asking some questions about the files in the ./data folder.
6. Do the same as step 5, but now uncomment `## 3. RAG and code execution assistant.`. This will add code execution on top of RAG. Now you can ask questions like, can you plot all employees on a graph according to their job title.