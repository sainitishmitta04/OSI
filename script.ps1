# ============================================================
#   MCP AI Applications - Windows Setup Script
# ============================================================

Set-ExecutionPolicy Bypass -Scope Process -Force

Write-Host ""
Write-Host "============================================"
Write-Host "      MCP AI Applications - Setup Script"
Write-Host "      Windows Environment"
Write-Host "============================================"
Write-Host ""

# 1. Check Python
Write-Host "Checking Python installation..."
python --version
pip --version
Write-Host "Note: Python must be installed manually."

# 2. Check Node.js
Write-Host ""
Write-Host "Checking Node.js installation..."
node -v
npm -v
npx -v
Write-Host "Note: Node.js must be installed manually."

# 3. Ensure npm version 11.6.2
Write-Host ""
Write-Host "Checking npm version..."

$currentNpm = npm -v

if ($currentNpm -ne "11.6.2") {
    Write-Host "Updating npm to version 11.6.2..."
    npm install -g npm@11.6.2
} else {
    Write-Host "npm is already at version 11.6.2"
}

npm -v

# 4. Install Google Gemini CLI **ONLY IF NOT INSTALLED**
Write-Host ""
Write-Host "Checking Gemini CLI..."

$geminiExists = Get-Command gemini -ErrorAction SilentlyContinue

if ($null -eq $geminiExists) {
    Write-Host "Gemini CLI not found. Installing Google Gemini CLI version 0.16.0..."
    npm install -g @google/gemini-cli@0.16.0
} else {
    Write-Host "Gemini CLI already installed."
}

# Show version only if command exists
$geminiExists = Get-Command gemini -ErrorAction SilentlyContinue
if ($geminiExists) {
    gemini --version
}

# 5. Install MCP Inspector
Write-Host ""
Write-Host "Installing MCP Inspector..."
npm install -g @modelcontextprotocol/inspector
#npx @modelcontextprotocol/inspector --version

# 6. Install uv 0.9.6
Write-Host ""
Write-Host "Installing uv version 0.9.6..."
pip install uv==0.9.6
uv --version

Write-Host ""
Write-Host "============================================"
Write-Host "   MCP Environment Setup Completed"
Write-Host "   npm is 11.6.2"
Write-Host "   Gemini CLI handled correctly"
Write-Host "   MCP Inspector installed"
Write-Host "   uv installed"
Write-Host "============================================"
Write-Host ""
