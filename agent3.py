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
key=os.getenv("cohere_api_key")


print("working. . .")

class AgentState(TypedDict):
    messages=Annotated[Sequence[BaseMessage],add_messages] # This field is a list of messages, and every time a new node runs, append new messages to the existing list using the add_messages function

@tool
def add(a:int, b:int):
    """  This is an addition function that adds 2 numbers together """
    return a+b
tools=[add]

#define model
model = ChatCohere(
    cohere_api_key=key,
    model="command-r",  # Make sure this is supported by the langchain-cohere version
    temperature=0.7
).bind_tools(tools)

print("working. . .")

def model_call(state: AgentState)->AgentState:
    system_prompt=SystemMessage(
        content="You are my AI assistant please answer my query to best of your ability")
    response=model.invoke([system_prompt]+state["messages"])
    return {"message":response}

def shouldContinue(state:AgentState):
    messages=state["messages"]
    last_message=messages[-1]
    if not last_message.tool_calls:
        return "end"
    else:
        return "continue"


graph=StateGraph(AgentState)
graph.add_node("our_agent", model_call)

tool_node=ToolNode(tools=tools)
graph.add_node("tools", tool_node)

graph.set_entry_point("our_agent")
graph.add_conditional_edges(
    "our_agent",
    shouldContinue,
    {
        "continue":"tools",
        "end":END,

    },

)

graph.add_edge("tools","our_agent")
app=graph.compile()

print("working . . . .")

def printStream(stream):
    for s in stream:
        message=s["messages"][-1]
        if isinstance(message,tuple):
            print(message)
        else:
            message.pretty_print()

inputs={"messages":[("user" ,"add 3+4")]}

x=app.stream(inputs, stream_mode="values")

printStream(x)

