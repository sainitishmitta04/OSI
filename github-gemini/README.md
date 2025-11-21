uv init .
uv venv
.venv\Scripts\activate
 
uv add fastmcp==2.11.3 mcp==1.13.1 certifi PyGithub python-dotenv
fastmcp version

# run directly
python main.py
 
# Register with Gemini CLI
gemini mcp add "." python main.py

# Verify and test
start gemini

# verify the tools 
gemini mcp list