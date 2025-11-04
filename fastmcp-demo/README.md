# fastmcp-demo - Utilities MCP Server

## Quick Setup

```powershell
cd C:\OSI\fastmcp-demo
uv init .
uv venv
.venv\Scripts\activate

uv add fastmcp==2.11.3 mcp==1.13.1
fastmcp version

# Test server
uv run fastmcp dev main.py

# Or run directly
python main.py

# Register with Gemini CLI
fastmcp install mcp-json main.py --project "C:\OSI\fastmcp-demo"
gemini mcp add demo-server uv -- run --project "C:\OSI\fastmcp-demo" --with fastmcp fastmcp run main.py

# Verify and test
gemini mcp list
gemini --prompt-interactive "Hello"
```
---
