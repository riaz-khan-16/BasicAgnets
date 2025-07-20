#step 1: define LLM

import os
from dotenv import load_dotenv
from langchain_cohere import ChatCohere

load_dotenv()
key=os.getenv("cohere_api_key")

llm = ChatCohere(
    cohere_api_key=key,
    model="command-r",  # Make sure this is supported by the langchain-cohere version
    temperature=0.7
)

print("LLM deifned. . . ")



#step 2: Make a custom tool

from langchain.tools import tool

@tool
def add_numbers(input: str) -> str:
    """Add two numbers given as 'a b'."""
    a, b = map(int, input.split())
    return str(a + b)

print("custom tool is made successully!")

#add it to tool list

tools = [add_numbers]


#step 3: Create the agent by using initialize_agent

from langchain.agents import initialize_agent, AgentType

agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION)

print("Agent is created successfully!")

result = agent.run("What is 154158415 + 545555  ?")
print(result)