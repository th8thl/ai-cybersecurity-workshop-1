# Setup

Use this file to get the vulnerable app running and configure model providers.

## Table Of Contents

- [Project Layout](#project-layout)
- [System Requirements](#system-requirements)
- [Install A Code Editor](#install-a-code-editor)
- [Install Python](#install-python)
- [Set Up GitHub For Your Portfolio](#set-up-github-for-your-portfolio)
- [GenAI Coding Help](#genai-coding-help)
- [Create `.env`](#create-env)
- [First-Time Setup](#first-time-setup)
- [Run After Setup](#run-after-setup)
- [The Three Model Providers](#the-three-model-providers)
- [Configure Gemini](#configure-gemini)
- [Configure Qwen With Ollama](#configure-qwen-with-ollama)
- [SQLite Chat History](#sqlite-chat-history)
- [Prompt Templates](#prompt-templates)
- [Run Tests](#run-tests)

## Project Layout

```text
starter/   Distribution code participants work with
solution/  Reference solution
```

Run participant work from the code folder unless an exercise explicitly asks you to compare against `solution/`.

## System Requirements

Required:

- a laptop where you can install software
- Windows 10/11, macOS, or Linux
- internet access
- enough permissions to install Python, Git, and a code editor
- enough local disk space for the workshop code and Python dependencies
- 8 GB RAM minimum

Approximate local disk space:

- workshop code and docs: under 100 MB
- Python virtual environment and dependencies: 300-700 MB
- optional Ollama install: about 1-2 GB
- optional Qwen model download: about 500 MB-1 GB for `qwen3:0.6b-q4_K_M`

Recommended free disk space: at least 3 GB without Ollama, or at least 6 GB if you plan to use Qwen locally.

Hardware notes:

- No GPU is required.
- 8 GB RAM is enough for the Django app and the mock provider.
- 16 GB RAM is recommended if you plan to run Qwen locally with Ollama while also running a browser, editor, and Django.
- The workshop Qwen model is intentionally small enough to run on CPU for classroom demos.

Bring or create:

- a GitHub account
- access to your email or authenticator app for GitHub login
- a browser for GitHub, Django, and optional GenAI browser chat

## Install A Code Editor

You need a text editor or IDE to inspect and change project files.

Recommended: Visual Studio Code

- Download: <https://code.visualstudio.com/>
- Install the Python extension from Microsoft.
- Open the code folder in VS Code before starting the exercises.

VS Code is recommended, not required. Any editor is fine if you can comfortably open and edit files:

- Notepad++
- Sublime Text
- PyCharm
- Cursor
- Windsurf
- Vim, Nano, or another terminal editor

## Install Python

Install Python before creating `.env` or running Django.

Use Python 3.11 or newer. If you already have Python installed, verify it first:

Windows PowerShell:

```powershell
python --version
py -3 --version
```

macOS or Linux:

```bash
python3 --version
```

If those commands do not show Python 3.11 or newer, install Python:

### Windows

Recommended options:

- Install from <https://www.python.org/downloads/windows/>.
- During install, check **Add python.exe to PATH**.
- Or install with `winget`:

```powershell
winget install Python.Python.3.12
```

After installing, close and reopen PowerShell, then verify:

```powershell
python --version
```

If `python` does not work but `py -3` does, use `py -3` wherever the setup shows `python`.

### macOS

Recommended options:

- Install from <https://www.python.org/downloads/macos/>.
- Or install with Homebrew:

```bash
brew install python
```

Then verify:

```bash
python3 --version
```

### Linux

Use your distro package manager.

Ubuntu or Debian:

```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip
python3 --version
```

Fedora:

```bash
sudo dnf install python3 python3-pip
python3 --version
```

## Set Up GitHub For Your Portfolio

You will use GitHub to keep a copy of your workshop work for your portfolio.

This section does three things:

- installs Git and GitHub CLI
- clones the workshop repository
- pushes your completed work to your own GitHub repository

### Install Git

Windows:

```powershell
winget install --id Git.Git
```

macOS:

```bash
brew install git
```

Linux:

```bash
sudo apt update
sudo apt install git
```

Verify:

```bash
git --version
```

### Install GitHub CLI

Windows:

```powershell
winget install --id GitHub.cli
```

macOS:

```bash
brew install gh
```

Linux:

```bash
sudo apt install gh
```

If your Linux package manager cannot find `gh`, use the official install instructions:

<https://github.com/cli/cli/blob/trunk/docs/install_linux.md>

Close and reopen your terminal, then verify:

```bash
gh --version
```

### Log In To GitHub

```bash
gh auth login
```

Choose:

- `GitHub.com`
- `HTTPS`
- `Login with a web browser`

Verify:

```bash
gh auth status
```

### Clone The Workshop Repository

Replace `<WORKSHOP_REPO_URL>` with the repository URL provided by the instructor.

Windows PowerShell:

```powershell
cd C:\Work\Codepath\Cybersecurity
git clone <WORKSHOP_REPO_URL>
cd <cloned-repo-folder>
```

macOS or Linux:

```bash
mkdir -p ~/codepath/cybersecurity
cd ~/codepath/cybersecurity
git clone <WORKSHOP_REPO_URL>
cd <cloned-repo-folder>
```

### Create Your Portfolio Repository

Create a new GitHub repository under your own account.

Recommended settings:

- repository name: `ai-security-workshop-1`
- visibility: public, if you want to show it in your portfolio
- do not initialize it with a README, `.gitignore`, or license if you are pushing this cloned workshop folder directly

Copy the new repository URL. It will look like:

```text
https://github.com/YOUR-USERNAME/ai-security-workshop-1.git
```

### Push Your Work To Your Repository

After you complete the workshop exercises, commit your changes and push them to your own repo.

First, check that local-only files are ignored:

```bash
git status --short
```

Do not commit:

```text
.env
db.sqlite3
.venv/
__pycache__/
```

Then commit:

```bash
git add .
git commit -m "Complete AI security workshop 1"
```

Point `origin` at your own repository:

```bash
git remote set-url origin <YOUR_REPO_URL>
```

Push:

```bash
git push -u origin main
```

If your default branch is named `master`, use:

```bash
git push -u origin master
```

## GenAI Coding Help

Some exercises include optional prompts for using GenAI to help implement code changes.

There are two supported workflows:

### IDE Coding Agent

Use this path if you have an AI coding agent installed in VS Code, Cursor, Windsurf, or another IDE.

The agent can usually read files directly from the workspace and produce edits in place. In the exercises, use the **IDE coding-agent prompt** and make sure the agent is pointed at the code folder.

Before accepting changes:

- read the diff
- make sure it changed only the requested files
- run the verification commands from the exercise

### Browser Chat

Use this path if you are using ChatGPT, Claude, Gemini, or another web chat.

The browser chat cannot see your local files unless you paste them. In the exercises, use the **browser chat context** block first, paste each listed file with its filename header, then paste the **browser chat prompt**.

Ask the browser chat for one of these output formats:

- a unified diff
- complete replacement contents for a specific file
- small copy-paste snippets with exact filenames and locations

After applying the suggested changes, run the same verification commands as everyone else.

## Create `.env`

Before running Django, copy the template file and rename the copy to `.env`.

Windows PowerShell:

```powershell
cd C:\Work\Codepath\Cybersecurity\Session1_AI_Threat_Modeling_Input_Security\starter
Copy-Item .env.example .env
```

Windows Command Prompt:

```cmd
cd C:\Work\Codepath\Cybersecurity\Session1_AI_Threat_Modeling_Input_Security\starter
copy .env.example .env
```

macOS or Linux:

```bash
cd /path/to/Session1_AI_Threat_Modeling_Input_Security/starter
cp .env.example .env
```

Do not commit `.env`. It is a local settings file.

`DJANGO_SECRET_KEY` is required. The committed `.env.example` uses a placeholder so the workshop setup is easy to see, but each local `.env` should have its own value. After Python is installed, generate one:

```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

Paste the generated value into `.env`:

```text
DJANGO_SECRET_KEY=your-generated-local-value
```

The provider is selected in the app from the Provider dropdown. You do not need to set `AI_PROVIDER` in `.env` for the workshop. If the browser does not send a provider, Django falls back to the local mock provider.

## First-Time Setup

Run this once per machine or whenever you recreate the virtual environment. On Windows, `python` may also be available as `py -3`. On macOS or Linux, use `python3` if `python` is not available.

Create `.env` first using the commands above, then run the setup commands for your operating system.

Windows PowerShell:

```powershell
cd C:\Work\Codepath\Cybersecurity\Session1_AI_Threat_Modeling_Input_Security\starter
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
```

Windows Command Prompt:

```cmd
cd C:\Work\Codepath\Cybersecurity\Session1_AI_Threat_Modeling_Input_Security\starter
python -m venv .venv
.venv\Scripts\activate.bat
pip install -r requirements.txt
python manage.py migrate
```

macOS:

```bash
cd /path/to/Session1_AI_Threat_Modeling_Input_Security/starter
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python manage.py migrate
```

Linux:

```bash
cd /path/to/Session1_AI_Threat_Modeling_Input_Security/starter
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python manage.py migrate
```

## Run After Setup

Use this every time after first-time setup is complete.

Windows PowerShell:

```powershell
cd C:\Work\Codepath\Cybersecurity\Session1_AI_Threat_Modeling_Input_Security\starter
.\.venv\Scripts\Activate.ps1
python manage.py runserver
```

Windows Command Prompt:

```cmd
cd C:\Work\Codepath\Cybersecurity\Session1_AI_Threat_Modeling_Input_Security\starter
.venv\Scripts\activate.bat
python manage.py runserver
```

macOS:

```bash
cd /path/to/Session1_AI_Threat_Modeling_Input_Security/starter
source .venv/bin/activate
python manage.py runserver
```

Linux:

```bash
cd /path/to/Session1_AI_Threat_Modeling_Input_Security/starter
source .venv/bin/activate
python manage.py runserver
```

Open `http://127.0.0.1:8000`.
## The Three Model Providers

| Provider | Where it runs | What it is for | Configuration |
| --- | --- | --- | --- |
| `mock` | Inside the Django app | A deterministic classroom provider with hardcoded behavior. It is intentionally easy to demonstrate. | No extra setup. |
| `qwen` | Locally through Ollama at `http://localhost:11434` | A self-hosted model participants can run without a cloud API. Its answers can vary and may hallucinate. | Install Ollama and pull `qwen3:0.6b-q4_K_M`. |
| `gemini` | Managed Google Gemini API | A managed provider that is usually the most defensive in this workshop, which helps show that provider behavior is not the same as application security. | Add `GEMINI_API_KEY` to `.env`. |

Switch providers from the app's Provider dropdown.

## Configure Gemini

1. Go to <https://aistudio.google.com/apikey>.
2. Create an API key.
3. Open `.env` in the code folder.
4. Set these values:

```text
GEMINI_API_KEY=your-real-key-here
GEMINI_MODEL=gemini-3.6-flash
```

Restart Django after editing `.env`.

## Configure Qwen With Ollama

The app sends Qwen requests to Ollama's local chat API.

### Windows

1. Download Ollama from <https://ollama.com/download>.
2. Run the Windows installer.
3. Open PowerShell.
4. Verify Ollama:

```powershell
ollama --version
```

5. Pull the workshop model:

```powershell
ollama pull qwen3:0.6b-q4_K_M
```

### macOS

1. Download Ollama from <https://ollama.com/download>.
2. Open the macOS app.
3. Open Terminal.
4. Verify Ollama:

```bash
ollama --version
```

5. Pull the workshop model:

```bash
ollama pull qwen3:0.6b-q4_K_M
```

### Linux

```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama --version
ollama pull qwen3:0.6b-q4_K_M
```

The default Qwen settings are already in `.env.example`:

```text
QWEN_MODEL=qwen3:0.6b-q4_K_M
QWEN_API_URL=http://localhost:11434/api/chat
```

### Verify Qwen

First confirm the model is installed:

Windows PowerShell:

```powershell
ollama list
```

macOS or Linux:

```bash
ollama list
```

You should see `qwen3:0.6b-q4_K_M` in the list.

Then run a one-sentence local model check:

Windows PowerShell:

```powershell
ollama run qwen3:0.6b-q4_K_M "Explain what a firewall is in one sentence."
```

macOS or Linux:

```bash
ollama run qwen3:0.6b-q4_K_M "Explain what a firewall is in one sentence."
```

Finally, verify the same local chat API endpoint the Django app uses.

Windows PowerShell:

```powershell
$body = @{
    model = "qwen3:0.6b-q4_K_M"
    messages = @(
        @{
            role = "user"
            content = "Explain what a firewall is in one sentence."
        }
    )
    stream = $false
} | ConvertTo-Json -Depth 5

Invoke-RestMethod `
    -Uri "http://localhost:11434/api/chat" `
    -Method Post `
    -ContentType "application/json" `
    -Body $body
```

macOS or Linux:

```bash
curl http://localhost:11434/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen3:0.6b-q4_K_M",
    "messages": [
      {
        "role": "user",
        "content": "Explain what a firewall is in one sentence."
      }
    ],
    "stream": false
  }'
```

If the API check works, start Django, select `qwen` in the Provider dropdown, and send a normal prompt.

## SQLite Chat History

Django stores workshop chat messages in `db.sqlite3`.

The chat table is:

```text
chatbot_chatmessage
```

For this workshop, messages are intentionally stored one by one in plaintext. That lets participants inspect chat history directly and leaves memory isolation and encryption at rest for later workshops.

To inspect the database visually, install DB Browser for SQLite from <https://sqlitebrowser.org/dl/>. Open `db.sqlite3` in the code folder, then browse `chatbot_chatmessage`.

## Run Tests

From the code folder:

```bash
python manage.py test
```

From `solution/`:

```bash
python manage.py test
```







