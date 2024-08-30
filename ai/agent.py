from dotenv import load_dotenv

load_dotenv()
import os

from typing import List, Dict
from langchain.agents import initialize_agent, Tool, AgentType
from langchain_openai import ChatOpenAI
from langchain.tools.base import StructuredTool
from langchain.agents import create_tool_calling_agent
from langchain.agents import AgentExecutor
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from ai.db_tool import DBTool, DB_DESCRIPTION


db_tool = DBTool()
model = ChatOpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"), model="gpt-4o")

def search_in_db(user_question: str):
    """Sends the user's question to an AI subsystem capable of understanding the question and retrieving data from the database. Use only if the user asks about the customers data."""
    return db_tool(user_question)


def explain_data(user_question: str):
    """Answers questions about the data definition: column names and their description. Use when the user asks about a column content or wants to know the name of the column based on the provided description."""

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You help the user to understand the data."),
        ("system", "Given the user's question provide the description of the mentioned columns or find the column name with the provided description."),
        ("system", "Available data: " + DB_DESCRIPTION),
        ("human", "{input}"),
    ])

    chain = prompt | model | StrOutputParser()
    return chain.invoke({"input": user_question})


tools = [
    StructuredTool.from_function(search_in_db),
    StructuredTool.from_function(explain_data)
]

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an AI assistant who helps with customer data."),
    ("system", "You have access to two tools: search_in_db and explain_data."),
    ("system", "You can use search_in_db if the user asks about the customers data."),
    ("system", "You can use explain_data if the user asks about the data definition: column names and their description."),
    ("system", "If you are not sure which tool to use, ask the user to clarify the question."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad")
])

def run_agent(user_question: str, external_history: List[Dict[str, str]]):
    memory = ConversationBufferMemory(memory_key="chat_history")

    for message in external_history:
        if message["role"] == "user":
            memory.chat_memory.add_user_message(message["content"])
        elif message["role"] == "assistant":
            memory.chat_memory.add_ai_message(message["content"])

    agent = create_tool_calling_agent(model, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, max_iterations=4, verbose=True)

    agent_with_message_history = RunnableWithMessageHistory(
        agent_executor,
        lambda session_id: memory.chat_memory, # tutaj powinniśmy wczytywać historię z bazy danych
        input_messages_key="input",
        history_messages_key="chat_history"
    )

    result = agent_with_message_history.invoke(
        {"input": user_question},
        config={"configurable": {"session_id": "123"}}
    )

    return result["output"]