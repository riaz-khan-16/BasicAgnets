#Now we will build and agent with memory

from langgraph.graph import StateGraph, START, END
import os
from dotenv import load_dotenv
from langchain_cohere import ChatCohere
from langchain_core.messages import HumanMessage, AIMessage
from typing import TypedDict, List, Union


load_dotenv()
key=os.getenv("cohere_api_key")

llm = ChatCohere(
    cohere_api_key=key,
    model="command-r",  # Make sure this is supported by the langchain-cohere version
    temperature=0.7
)

print("LLM deifned. . . ")

class AgentState(TypedDict):
    message:List[Union[HumanMessage,AIMessage]]

    

def process(state:AgentState)->AgentState:
    response=llm.invoke(state["message"])
    state["message"].append(AIMessage(content=response.content))
    print(response.content)
    return state


print("Now define the graph")
graph=StateGraph(AgentState)
graph.add_node("process", process)
graph.add_edge(START,"process")
graph.add_edge("process",END)
agent=graph.compile()

print("graph is defined")

conversation_history=[]

user_input=input("Enter: ")   
while user_input!="exit":
    conversation_history.append(HumanMessage(content=user_input))
    result=agent.invoke({"message": conversation_history})
    
    conversation_history=result['message']
    user_input=input("User: ")  


print("working. . . ")

with open("log.txt", "w") as file:
    file.write("Your conversation log: \n")

    for message in conversation_history:
        if isinstance(message,HumanMessage):
             file.write("You: "+message.content+"\n")
        elif isinstance(message,AIMessage):
             file.write("AI: "+message.content+"\n\n")
    file.write("End of converation . . ")

print(conversation_history)

for message in conversation_history:
    print(message.content)

print("conversation is saved")
        
          
        

