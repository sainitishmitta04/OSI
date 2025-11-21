# main.py
import os
import ssl
import certifi

from mcp.server.fastmcp import FastMCP
from github import Github, Auth
from dotenv import load_dotenv

# ---------------------------------------------------------------------
# SSL FIX (Required for Windows & corporate networks)
# ---------------------------------------------------------------------
cafile = certifi.where()
os.environ["SSL_CERT_FILE"] = cafile
os.environ["REQUESTS_CA_BUNDLE"] = cafile

ssl_context = ssl.create_default_context(cafile=cafile)
ssl._create_default_https_context = lambda *args, **kwargs: ssl_context

# ---------------------------------------------------------------------
# Initialize MCP Server
# ---------------------------------------------------------------------
mcp = FastMCP("github-mcp-server")

# Load GitHub Token
load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

if not GITHUB_TOKEN:
    raise RuntimeError("Missing GITHUB_TOKEN in your .env file")

auth = Auth.Token(GITHUB_TOKEN)
gh = Github(auth=auth)

# ---------------------------------------------------------------------
# GitHub MCP Tools
# ---------------------------------------------------------------------

@mcp.tool()
def create_repository(repo_name: str, private: bool = False, description: str = "") -> str:
    """
    Create a new GitHub repository under the authenticated user's account.
    """
    user = gh.get_user()
    repo = user.create_repo(
        name=repo_name,
        description=description,
        private=private,
        auto_init=True
    )
    return f"Repository '{repo_name}' created successfully at {repo.html_url}"


@mcp.tool()
def create_branch(repo_name: str, base_branch: str, new_branch: str) -> str:
    """
    Create a new branch from an existing base branch.
    """
    repo = gh.get_repo(repo_name)
    base = repo.get_branch(base_branch)

    repo.create_git_ref(ref=f"refs/heads/{new_branch}", sha=base.commit.sha)
    return f"Branch '{new_branch}' created from '{base_branch}'."


@mcp.tool()
def create_file(repo_name: str, branch: str, file_path: str, content: str, commit_message: str) -> str:
    """
    Create or update a file inside a GitHub repository.
    """
    repo = gh.get_repo(repo_name)

    try:
        existing = repo.get_contents(file_path, ref=branch)
        repo.update_file(existing.path, commit_message, content, existing.sha, branch=branch)
        return f"Updated file '{file_path}' on branch '{branch}'."
    except Exception:
        repo.create_file(file_path, commit_message, content, branch=branch)
        return f"Created new file '{file_path}' on branch '{branch}'."


@mcp.tool()
def create_pull_request(repo_name: str, base: str, head: str, title: str, body: str = "") -> str:
    """
    Create a pull request.
    """
    repo = gh.get_repo(repo_name)
    pr = repo.create_pull(title=title, body=body, base=base, head=head)
    return f"Pull request created: {pr.html_url}"


@mcp.tool()
def summarize_repository(repo_name: str) -> str:
    """
    Summarize a GitHub repository:
    - Basic info
    - Languages
    - Approx file count
    - Recent commit messages
    """
    repo = gh.get_repo(repo_name)

    name = repo.full_name
    description = repo.description or "No description"
    stars = repo.stargazers_count
    forks = repo.forks_count
    open_issues = repo.open_issues_count

    # Language summary
    langs = repo.get_languages()
    if langs:
        total = sum(langs.values())
        lang_summary = ", ".join([f"{k} ({v * 100 / total:.1f}%)" for k, v in langs.items()])
    else:
        lang_summary = "No languages detected"

    # Approx file count (limited to avoid API throttling)
    contents = repo.get_contents("")
    file_count = 0
    while contents:
        item = contents.pop(0)
        if item.type == "dir":
            contents.extend(repo.get_contents(item.path))
        else:
            file_count += 1
            if file_count >= 200:
                break

    # Recent commits
    commits = repo.get_commits()
    commit_msgs = [c.commit.message.split("\n")[0] for c in commits[:3]]
    commit_summary = "; ".join(commit_msgs) if commit_msgs else "No commits found"

    return (
        f"Repository: {name}\n"
        f"Description: {description}\n"
        f"Stars: {stars}, Forks: {forks}, Open Issues: {open_issues}\n"
        f"Languages: {lang_summary}\n"
        f"Approx. Files: {file_count}\n"
        f"Recent Commits: {commit_summary}"
    )


@mcp.tool()
def delete_repository(repo_name: str) -> str:
    """
    Delete a GitHub repository owned by the authenticated user.
    """
    try:
        repo = gh.get_repo(repo_name)
        repo.delete()
        return f"Repository '{repo_name}' deleted successfully."
    except Exception as e:
        return f"Failed to delete repository '{repo_name}': {e}"


# ---------------------------------------------------------------------
# MCP Run
# ---------------------------------------------------------------------
if __name__ == "__main__":
    mcp.run()
