from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage
from langgraph.graph import StateGraph, END
from mcp_tools import save_analysis_report  # Direct call to your MCP tool function

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], "The conversation history"]
    next_step: str

def orchestrator_node(state: AgentState):
    """Evaluates user intent and routes to specialized worker."""
    last_message = state["messages"][-1].content.lower()
    
    if "code" in last_message or "script" in last_message or "save" in last_message:
        return {"next_step": "coder"}
    return {"next_step": "researcher"}

def researcher_node(state: AgentState):
    """Executes research synthesis."""
    user_query = state["messages"][0].content
    # Simulated analysis logic or LLM call result
    summary = f"Analysis for query '{user_query}': Identified 3 core growth metrics in Q3 data."
    return {"messages": list(state["messages"]) + [SystemMessage(content=summary)]}

def coder_node(state: AgentState):
    """Executes code generation and calls the FastMCP file saver tool."""
    user_query = state["messages"][0].content
    report_content = f"# Generated Report\n\nQuery Processed: {user_query}\nStatus: Successfully validated."
    
    # Executing the local FastMCP tool call directly
    tool_result = save_analysis_report("output_report.md", report_content)
    
    return {"messages": list(state["messages"]) + [SystemMessage(content=tool_result)]}

# Build State Graph
workflow = StateGraph(AgentState)
workflow.add_node("orchestrator", orchestrator_node)
workflow.add_node("researcher", researcher_node)
workflow.add_node("coder", coder_node)

workflow.set_entry_point("orchestrator")

workflow.add_conditional_edges(
    "orchestrator",
    lambda state: state["next_step"],
    {"researcher": "researcher", "coder": "coder"}
)

workflow.add_edge("researcher", END)
workflow.add_edge("coder", END)

app = workflow.compile()