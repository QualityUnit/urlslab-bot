RAG_CHAT_TEMPLATE = """Reply to human input with the following context or your general knowledge and the history of
chat conversation.: 
CONTEXT START: 
{context}
CONTEXT END

CHAT HISTORY START:
{history}
CHAT HISTORY END

Human input: {human_input}
"""
