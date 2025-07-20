from langgraph.graph import StateGraph, START, END
import os
from dotenv import load_dotenv
from langchain_cohere import ChatCohere
from langchain_core.messages import HumanMessage
from typing import TypedDict, List


load_dotenv()
key=os.getenv("cohere_api_key")

llm = ChatCohere(
    cohere_api_key=key,
    model="command-r",  # Make sure this is supported by the langchain-cohere version
    temperature=0.7
)

print("LLM deifned. . . ")

class AgentState(TypedDict):
    message:List[HumanMessage]
    

def process(state:AgentState)->AgentState:
    response=llm.invoke(state["message"])
    print(response.content)
    return state

print("Now define the graph")
graph=StateGraph(AgentState)
graph.add_node("process", process)
graph.add_edge(START,"process")
graph.add_edge("process",END)
agent=graph.compile()

print("graph is defined")

user_input=input("Enter: ")   
while user_input!="exit":
    agent.invoke({"message": [HumanMessage(content=user_input)]})
    user_input=input("User: ")  


print("working. . . ")