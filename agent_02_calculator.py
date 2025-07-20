# make the same agent using Langgraph
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



#step 1: Define the LLM
load_dotenv()
key=os.getenv("cohere_api_key")
model = ChatCohere(
    cohere_api_key=key,
    model="command-r",  # Make sure this is supported by the langchain-cohere version
    temperature=0.7
)
print("Model is defined . . . . ")


#step 2: Define tool with docstring which is very important

@tool
def add(a:int, b:int):
    """  This is an addition function that adds 2 numbers together """
    return a+b
@tool
def sub(a:int, b:int):
    """  This is an addition function that subtracts 2 numbers """
    return a-b
@tool
def div(a:int, b:int):
    """  This is an addition function that divides 2 numbers """
    return a/b
@tool
def mul(a:int, b:int):
    """  This is an addition function that multiplies 2 numbers """
    return a*b

tools=[add,sub]
model.bind_tools(tools) # Bind it with the model: It will say the model that we have these tools

print("Tools are defined and bined . . . ")


#Step 3: This will store our conversation history in a structured way

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

print("state is created . . ")

#Step 4: Now create nodes for our graph of the agent

# Node1: make a node for calling model: this will call our LLM
def model_call(state: AgentState)->AgentState:
    system_prompt=SystemMessage(
        content="You are my AI assistant please answer my query to best of your ability")
    response=model.invoke([system_prompt]+state['messages'])
    return {"messages": [response]}

#Node2: If there is no tool call, it will end
def shouldContinue(state:AgentState):
   
    messages=state["messages"]
    last_message=messages[-1]
    if not last_message.tool_calls:
        return "end"
    else:
        return "continue"


#Step4: Now define your graph
print("Graph is being created... ")
graph=StateGraph(AgentState)
graph.add_node("model_call", model_call)
tool_node=ToolNode(tools=tools)
graph.add_node("tools", tool_node)

#add starting node
graph.set_entry_point("model_call")

#add conditional edge from model_Call to shouldContinue
graph.add_conditional_edges(
    "model_call", 
    shouldContinue,    
    {
        "continue":"tools",  # if shouldContinue model return "continue" this will go to tools node
        "end":END,  #  if shouldContinue model return "continue" this will go to END nodes

    },

)


graph.add_edge("tools","model_call") # add an edge from tools to model call
app=graph.compile()
print("Graph is compiled Successfully!")


inputs={"messages":[("user", "multiply 100, 2")]}
streams=app.stream(inputs, stream_mode='values')


def printStream(stream):
    for s in stream:
        message=s["messages"][-1]
        if isinstance(message,tuple):
            print(message)
        else:
            message.pretty_print()

printStream(streams)

