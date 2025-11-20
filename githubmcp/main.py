# main.py
from mcp.server.fastmcp import FastMCP
from github import Github
from dotenv import load_dotenv
import os

# Initialize MCP app
mcp = FastMCP("github-mcp")

# Load GitHub token
load_dotenv() 
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    raise RuntimeError("Missing GITHUB_TOKEN environment variable")

gh = Github(GITHUB_TOKEN)

@mcp.tool()
def create_repository(repo_name: str, private: bool = False, description: str = "") -> str:
    """
    Create a new GitHub repository under the authenticated user's account.
    Args:
        repo_name: str -> The name of the new repository
        private: bool -> Whether the repository should be private
        description: str -> Optional description of the repository
    Returns:
        str -> Confirmation message with repository URL
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
def create_branch(repo_name: str, base_branch: str, new_branch: str):
    """Create a new branch in the specified GitHub repository."""
    repo = gh.get_repo(repo_name)
    base = repo.get_branch(base_branch)
    repo.create_git_ref(ref=f"refs/heads/{new_branch}", sha=base.commit.sha)
    return f"Branch '{new_branch}' created from '{base_branch}'."


@mcp.tool()
def create_file(repo_name: str, branch: str, file_path: str, content: str, commit_message: str):
    """Create or update a file in the given GitHub repository."""
    repo = gh.get_repo(repo_name)
    try:
        existing = repo.get_contents(file_path, ref=branch)
        repo.update_file(existing.path, commit_message, content, existing.sha, branch=branch)
        msg = f"Updated file '{file_path}' on branch '{branch}'."
    except Exception:
        repo.create_file(file_path, commit_message, content, branch=branch)
        msg = f"Created new file '{file_path}' on branch '{branch}'."
    return msg


@mcp.tool()
def create_pull_request(repo_name: str, base: str, head: str, title: str, body: str = ""):
    """Create a pull request in the specified GitHub repository."""
    repo = gh.get_repo(repo_name)
    pr = repo.create_pull(title=title, body=body, base=base, head=head)
    return f"Pull request created: {pr.html_url}"

@mcp.tool()
def summarize_repository(repo_name: str) -> str:
    """
    Summarize a GitHub repository.
    Args:
        repo_name: str -> Example: "delegate-org/awesome-project"
    Returns:
        str summary
    """
    repo = gh.get_repo(repo_name)

    # Basic info
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

    # File count (limited for performance)
    contents = repo.get_contents("")
    file_count = 0
    while contents:
        file = contents.pop(0)
        if file.type == "dir":
            contents.extend(repo.get_contents(file.path))
        else:
            file_count += 1
            if file_count >= 200:
                break  # stop early to avoid hitting API limits

    # Recent commits
    commits = repo.get_commits()
    commit_messages = [c.commit.message.split("\n")[0] for c in commits[:3]]
    commit_summary = "; ".join(commit_messages) if commit_messages else "No commits found"

    summary = (
        f"Repository: {name}\n"
        f"Description: {description}\n"
        f"Stars: {stars}, Forks: {forks}, Open Issues: {open_issues}\n"
        f"Languages: {lang_summary}\n"
        f"Approx. Files: {file_count}\n"
        f"Recent Commits: {commit_summary}"
    )

    return summary

@mcp.tool()
def delete_repository(repo_name: str) -> str:
    """
    Delete a GitHub repository owned by the authenticated user.
    Args:
        repo_name: str -> Example: "username/repository-name"
    Returns:
        str -> Confirmation message
    """
    try:
        repo = gh.get_repo(repo_name)
        repo.delete()
        return f"Repository '{repo_name}' deleted successfully."
    except Exception as e:
        return f"Failed to delete repository '{repo_name}': {e}"


if __name__ == "__main__":
    mcp.run()
