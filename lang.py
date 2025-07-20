
import os
from dotenv import load_dotenv
load_dotenv()
key=os.getenv("cohere_api_key")
from langchain_cohere import ChatCohere
from langchain_core.messages import HumanMessage
# chat = ChatCohere()
# messages = [HumanMessage(content="knock knock")]
# print(chat.invoke(messages))

llm = ChatCohere(
    cohere_api_key=key,
    model="command-r",  # Make sure this is supported by the langchain-cohere version
    temperature=0.7
)

response = llm.invoke("Explain the difference between AI and Machine Learning.")
print(response.content)
