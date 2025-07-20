from langgraph.graph import StateGraph, START, END
import os
from dotenv import load_dotenv
from langchain_cohere import ChatCohere
from langchain_core.messages import HumanMessage, AIMessage
from typing import TypedDict, List, Union,Annotated,Sequence
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage, SystemMessage
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode


load_dotenv()

load_dotenv()
key=os.getenv("cohere_api_key")


print("working. . .")

class AgentState(TypedDict):
    messages=Annotated[Sequence[BaseMessage],add_messages] # This field is a list of messages, and every time a new node runs, append new messages to the existing list using the add_messages function


@tool
def update(content:str)->str:
    """Updates the document with the provided content"""
