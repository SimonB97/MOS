# AI Task Runner

Run diverse complex tasks using AI agents (1) to write code, analyze files, and browse the web. Each task is broken down and handled by specialized AI agents with optional human oversight. Built on Microsoft's [MagenticOne](https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/magentic-one.html#), a generalist multi-agent system for solving complex tasks.

(1) "Agent" meaning the system described under *Agents*  in Antropic's "[Building effective agents](https://www.anthropic.com/research/building-effective-agents)"

## Requirements

- Python 3.8 or higher
- [uv](https://github.com/astral-sh/uv) installed
- OpenAI API key (set as OPENAI_API_KEY environment variable)

## Usage

Set up OpenAI API key first (see [below](#setting-up-openai-api-key)).

Basic usage:
```bash
uv run m1.py "look at the contents of these pdfs and rename them based on that"
```

With web browsing:
```bash
uv run --with-extras web m1.py "add index numbers for the songs in the album in this directory" -w
```

Without human oversight (disable Human-in-the-Loop):
```bash
uv run m1.py "your task" --no-hil
```

**Note:** When using `uv`, you can run directly without downloading:
```bash
uv run https://raw.githubusercontent.com/SimonB97/MOS/main/AITaskRunner/m1.py "your task" [options]
```

### Setting up OpenAI API key

Set the OpenAI API key as an environment variable:

a) **Linux/macOS:**
```bash
export OPENAI_API_KEY="your-api-key"
```

b) **Windows:**

1. Press Win+R and run the following command (opens Environment Variables window):
```
rundll32 sysdm.cpl,EditEnvironmentVariables
```
2. Under 'User variables', click 'New' and enter your API key
3. (Restart the command-line interface)

**Alternatively**, you can set the environment variable in the command prompt:

```cmd
set OPENAI_API_KEY="your-api-key"
```
(will be set for the current session only)

## Features

- Uses specialized AI agents for different task aspects
- File system operations (enabled by default)
- Code writing and execution (enabled by default)
- Web browsing with `-w/--web` (requires `--with-extras web`)
- Human oversight mode (enabled by default, disable with `--no-hil`)
- Preserves file system safety with explicit approvals
