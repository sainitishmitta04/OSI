mkdir fastmcp-demo
cd fastmcp-demo

uv init .
uv venv
.\.venv\Scripts\activate

uv add fastmcp==2.11.3 mcp==1.13.1

fastmcp version
