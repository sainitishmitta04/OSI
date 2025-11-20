# dbmcp - Database MCP Server

## Quick Setup

```powershell
cd C:\OSI\dbmcp
uv init .
uv venv
.venv\Scripts\activate

uv add fastmcp==2.11.3 mcp==1.13.1 sqlalchemy
fastmcp version

# Test server
uv run fastmcp dev main.py

# Or run directly
python main.py

# Register with Gemini CLI
fastmcp install mcp-json main.py --project "$PWD"
gemini mcp add demo-server uv -- run --project "$PWD" --with fastmcp fastmcp run main.py

# Register with claude desktop
fastmcp install claude-desktop main.py --project "$PWD"

# Verify and test
gemini mcp list
gemini --prompt-interactive "Hello"
```

## .env File
Create `.env` file in the project root:
```
GEMINI_API_KEY=
```


