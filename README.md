# 🧠 MCP AI Applications — Full Windows Setup Guide

This repository contains multiple MCP AI projects:

- `dbmcp` — MCP for Database interactions
- `fastmcp-demo` — MCP for small utilities (dice roll, temperature, time, etc.)
- `mcptest` — MCP for API-based tasks (e.g., weather)

This guide walks you through setting up **everything from scratch** on a **Windows laptop**.

---

## 📋 Prerequisites

Before starting, ensure your Windows laptop meets the following:

- Internet connection
- PowerShell installed (default in Windows 10+)
- Optional: Git (for cloning repository)
- VS Code

---

## 1️⃣ Install Python 3.10+

1. Download Python 3.10+ from the official site: [https://www.python.org/downloads/windows/](https://www.python.org/downloads/windows/)
2. During installation:
   - ✅ Check "Add Python 3.10+ to PATH"
   - Choose **Customize installation → Next → Install**
3. Verify installation in PowerShell:

```powershell
python --version
pip --version
```

---

## 2️⃣ Install Node.js & npm

1. Download Node.js LTS (Windows x64) from [https://nodejs.org/en/download/](https://nodejs.org/en/download/)
2. Install with default options:
   - ✅ Ensure "Add to PATH" is checked
3. Verify installation in PowerShell:

```powershell
node -v
npm -v
npx -v
```

### 🔄 Update npm if Outdated

If versions are outdated:

```powershell
npm install -g npm@latest
npm -v
```

> Should show **11.6.2** or later.

```powershell
npm cache clean --force
```

---

## 3️⃣ Install Required Node.js Packages

After Node.js installation, install these essential packages:

### 🧭 Install MCP Inspector

```powershell
npm install -g @modelcontextprotocol/inspector@0.17.2
npx @modelcontextprotocol/inspector --version
```

> Should print `0.17.2`

### Install Google Gemini CLI

```powershell
npm install -g @google/gemini-cli
gemini --version
```

---

## 4️⃣ Install `uv`

`uv` is required for FastMCP setup.

```powershell
pip install uv
uv --version
```

---

## 5️⃣ Create Project Folder

```powershell
mkdir C:\OSI
cd C:\OSI
```

You can place all sub-projects (`dbmcp`, `fastmcp-demo`, `mcptest`) here.

---

## 6️⃣ Initialize & Prepare Python Virtual Environment

For each sub-project (repeat for `dbmcp`, `fastmcp-demo`, `mcptest`):

```powershell
cd <sub-project-folder>   # e.g., cd dbmcp
uv init .
uv venv
.venv\Scripts\activate
```

> Make sure virtual environment is **activated** before installing dependencies.

---

## 7️⃣ Install Project Dependencies

```powershell
uv add fastmcp==2.11.3 mcp==1.13.1
fastmcp version
```

---

## 8️⃣ Run FastMCP Dev Server

```powershell
uv run fastmcp dev main.py
```

* This starts the MCP dev server locally.
* Use **MCP Inspector** to test tools.

---

## 9️⃣ Test with MCP Inspector

* Open MCP Inspector.
* Set **Transport = stdio** → Connect → List Tools → Test tools.

---

## 🔑 1️⃣0️⃣ Create `.env` File for Gemini API Key

1. Create `.env` in project folder:

```text
GEMINI_API_KEY=YOUR_GOOGLE_AI_API_KEY
```

2. Load environment variables in PowerShell:

```powershell
Get-Content .env | ForEach-Object { 
    $pair = $_ -split '='; 
    [System.Environment]::SetEnvironmentVariable($pair[0], $pair[1], "Process") 
}
```

> Get your Google AI API Key from [https://aistudio.google.com](https://aistudio.google.com/app/api-keys)

---

## 1️⃣1️⃣ Install MCP JSON Server for Gemini

For each sub-project:

```powershell
fastmcp install mcp-json main.py --project "C:\OSI\<sub-project-folder>"
```

---

## 1️⃣2️⃣ Add MCP Server to Gemini CLI

```powershell
gemini mcp add <server-name> uv -- run --project "C:\OSI\<sub-project-folder>" --with fastmcp fastmcp run main.py
```

* Replace `<server-name>` with something meaningful:

  * dbmcp → `db-server`
  * fastmcp-demo → `demo-server`
  * mcptest → `weather-server`

---

## 1️⃣3️⃣ Verify MCP Servers

```powershell
gemini mcp list
```

* Confirms all MCP servers are registered.

---

## 🧠 1️⃣4️⃣ Start the Servers

### Option 1: Using Two Windows (Recommended for Testing)

**In Window 1:**
Start the MCP server:
```powershell
cd C:\OSI\<sub-project-folder>
python main.py
```

**In Window 2:**
Start the Gemini CLI (as MCP client):
```powershell
cd C:\OSI\<sub-project-folder>
gemini --prompt-interactive "Hello"
```

### Option 2: Using FastMCP Dev Server

```powershell
uv run fastmcp dev main.py
```

---

## 1️⃣5️⃣ Test Gemini CLI Interactively

```powershell
gemini --prompt-interactive "Hello"
```

* Should interact with the MCP server and respond using the registered tools.

---

## ✅ 1️⃣6️⃣ Verify Complete Setup

You should now have:

1. **Python 3.10+** installed and working
2. **Node.js & npm** installed and working (updated to latest versions)
3. **MCP Inspector & Gemini CLI** installed via npm
4. **uv** installed
5. **FastMCP + MCP libraries** installed
6. **Virtual environment** setup for each sub-project
7. **MCP Inspector** connected and listing tools
8. **Gemini CLI** connected to MCP servers
9. Ability to run all tools interactively via Gemini CLI
10. **Multiple server startup options** available

---

## ⚡ Optional: Useful Commands

* Activate virtual environment (PowerShell):

```powershell
.venv\Scripts\activate
```

* Run FastMCP dev server:

```powershell
uv run fastmcp dev main.py
```

* Install MCP JSON server:

```powershell
fastmcp install mcp-json main.py --project "C:\OSI\<sub-project-folder>"
```

* List MCP servers:

```powershell
gemini mcp list
```

* Test tools interactively:

```powershell
gemini --prompt-interactive "Hello"
```

* Clean npm cache:

```powershell
npm cache clean --force
```

---

This setup works for **all sub-projects** (`dbmcp`, `fastmcp-demo`, `mcptest`) and ensures your Windows laptop can run MCP AI projects fully.
