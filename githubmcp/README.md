# Github-MCP

## .env File
Create `.env` file in the project root:
```
GITHUB_TOKEN=<github_token>
```

## Installation Instructions
```
uv venv
.\.venv\Scripts\Activate.ps1         
python -m ensurepip --upgrade    
c:\Users\Administrator\Documents\MCP-tutorial\.venv\Scripts\python.exe -m pip install fastmcp PyGithub python-dotenv
pip show PyGithub      
python main.py    
```
claude_desktop_config.json
```
"github-mcp": {
    "command": "C:\\Users\\Administrator\\Documents\\MCP-tutorial\\.venv\\Scripts\\python.exe",
    "args": [
    "C:\\Users\\Administrator\\Documents\\MCP-tutorial\\main.py"
    ]
  }

```
