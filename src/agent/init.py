from ..models.llm import gemini as llm
from .tools import retrieve_notes, get_time, ddg
from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage, SystemMessage
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

# Define tools and model
tools = [retrieve_notes, get_time, ddg]
model = llm.bind_tools(tools)

# System prompt
SYSTEM_PROMPT = SystemMessage(
    content=(
        "You are a helpful assistant. "
        "Use the tools provided to answer user queries. "
        "If you need to retrieve notes, use the 'retrieve_notes' tool with the user's email. "
        "If you need the current time, use the 'get_time' tool. "
        "If you need to search the web, use the 'ddg' tool. "
        "Always respond with the most relevant information based on the user's query."
    )
)

def model_call(state: AgentState) -> AgentState:
    try:
        response = model.invoke([SYSTEM_PROMPT] + state["messages"])
        return {"messages": [response]}
    except Exception as e:
        error_message = f"Error invoking model: {e}"
        return {"messages": [SystemMessage(content=error_message)]}

def should_continue(state: AgentState):
    messages = state["messages"]
    last_message = messages[-1]
    if not hasattr(last_message, "tool_calls") or not last_message.tool_calls:
        return "end"
    return "continue"

# Define the graph
graph = StateGraph(AgentState)
graph.add_node("our_agent", model_call)
tool_node = ToolNode(tools=tools)
graph.add_node("tools", tool_node)
graph.set_entry_point("our_agent")
graph.add_conditional_edges(
    "our_agent",
    should_continue,
    {
        "continue": "tools",
        "end": END,
    },
)
graph.add_edge("tools", "our_agent")

# Compile with memory
memory = MemorySaver()
app = graph.compile(checkpointer=memory)