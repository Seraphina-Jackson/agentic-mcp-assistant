from agent_graph import app
from langchain_core.messages import HumanMessage

def run():
    query = "Research the latest growth trends and save a summary report."
    initial_state = {"messages": [HumanMessage(content=query)], "next_step": ""}
    
    output = app.invoke(initial_state)
    for msg in output["messages"]:
        print(f"[{msg.__class__.__name__}]: {msg.content}")

if __name__ == "__main__":
    run()