# Github MCP Server

## Quick Setup

```powershell
cd github-gemini
uv init .
uv venv
.venv\Scripts\activate

uv add fastmcp==2.11.3 mcp==1.13.1 certifi PyGithub python-dotenv
fastmcp version

# Test server
uv run fastmcp dev main.py

# Or run directly
python main.py
 
# Register with Gemini CLI
gemini mcp add "." python main.py

# Verify and test
start gemini

# verify the tools 
gemini mcp list

```

## .env File
Create `.env` file in the project root:
```
GITHUB_TOKEN=
GEMINI_API_KEY=
```




