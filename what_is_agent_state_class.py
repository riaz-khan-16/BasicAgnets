
from typing import Sequence, TypedDict
from typing_extensions import Annotated
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langgraph.graph import add_messages


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]


state: AgentState = {"messages": []}
print([m.content for m in state["messages"]])  # Output: []



new_state = {"messages": [HumanMessage(content="Hello, bot!")]}
state["messages"] = add_messages(state["messages"], new_state["messages"])

print([m.content for m in state["messages"]])
