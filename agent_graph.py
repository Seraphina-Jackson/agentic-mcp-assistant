from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END

# Define shared agent state
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], "The conversation history"]
    next_step: str

def orchestrator_node(state: AgentState):
    """Evaluates the prompt and decides whether to route to Researcher or Coder."""
    last_message = state["messages"][-1].content.lower()
    
    if "code" in last_message or "script" in last_message:
        return {"next_step": "coder"}
    return {"next_step": "researcher"}

def researcher_node(state: AgentState):
    """Handles analysis and research drafting."""
    # Simulated agent output for clarity
    res = "Research complete: Target dataset shows a 14% growth trend across Q3."
    return {"messages": list(state["messages"]) + [SystemMessage(content=res)]}

def coder_node(state: AgentState):
    """Handles code execution or tool writing tasks."""
    res = "Coder agent generated required script and validated syntax."
    return {"messages": list(state["messages"]) + [SystemMessage(content=res)]}

# Build the LangGraph State Machine
workflow = StateGraph(AgentState)

workflow.add_node("orchestrator", orchestrator_node)
workflow.add_node("researcher", researcher_node)
workflow.add_node("coder", coder_node)

workflow.set_entry_point("orchestrator")

# Conditional Edge routing
workflow.add_conditional_edges(
    "orchestrator",
    lambda state: state["next_step"],
    {
        "researcher": "researcher",
        "coder": "coder"
    }
)

workflow.add_edge("researcher", END)
workflow.add_edge("coder", END)

app = workflow.compile()