from fastmcp import FastMCP

# Create an MCP server instance
mcp = FastMCP("LocalWorkspaceTools")

@mcp.tool()
def save_analysis_report(filename: str, content: str) -> str:
    """Saves generated research or code analysis directly to a local file."""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    return f"Successfully saved output to {filename}"

if __name__ == "__main__":
    mcp.run()