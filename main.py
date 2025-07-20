
import cohere
import os 
from dotenv import load_dotenv
load_dotenv()
cohere_api_key=os.getenv("cohere_api_key")



co = cohere.ClientV2(cohere_api_key)
response = co.chat(
    model="command-a-03-2025", 
    messages=[{"role": "user", "content": "hello world!"}]
)

print(response)
