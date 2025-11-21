mkdir githubgemini
cd githubgemini

uv init .
uv venv
.\.venv\Scripts\activate

uv add fastmcp==2.11.3 mcp==1.13.1 certifi PyGithub python-dotenv

fastmcp version