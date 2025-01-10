# /// script
# requires-python = ">=3.8,<3.13"
# dependencies = [
#     "click>=8.0.0",
#     "autogen-agentchat==0.4.0",
#     "autogen-ext[magentic-one,openai]==0.4.0",
#     "rich>=13.7.0",
# ]
# [project.optional-dependencies]
# web = [
#     "autogen-ext[web]==0.4.0",
#     "playwright>=1.41.0",
# ]
# ///

import asyncio
import os
import sys
import warnings
from contextlib import asynccontextmanager
from typing import AsyncIterator, List

import click
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from autogen_agentchat.agents import AssistantAgent, CodeExecutorAgent
from autogen_agentchat.ui import Console as AgentConsole
from autogen_ext.agents.file_surfer import FileSurfer
from autogen_ext.agents.magentic_one import MagenticOneCoderAgent
from autogen_ext.agents.web_surfer import MultimodalWebSurfer
from autogen_ext.code_executors.local import LocalCommandLineCodeExecutor
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.teams.magentic_one import MagenticOne

# Suppress ResourceWarnings for now
warnings.filterwarnings('ignore', category=ResourceWarning)

# Create console that writes to stderr to avoid interfering with command output
console = Console(stderr=True)

def setup_openai_key() -> None:
    if not os.environ.get("OPENAI_API_KEY"):
        raise click.UsageError("OPENAI_API_KEY environment variable must be set")

def check_web_dependencies() -> None:
    try:
        import playwright
    except ImportError:
        script_path = click.get_current_context().params.get('script_path', 'script.py')
        raise click.UsageError(
            "Web features require additional dependencies. Install them with:\n"
            f"uv run --with-extras web {script_path} [args...]"
        )

def create_agents(client: OpenAIChatCompletionClient, web: bool = False, 
                 files: bool = True, code: bool = True) -> List[AssistantAgent]:
    agents: List[AssistantAgent] = []
    
    if web:
        check_web_dependencies()
        agents.append(MultimodalWebSurfer("WebSurfer", model_client=client))
    
    if files:
        agents.append(FileSurfer("FileSurfer", model_client=client))
    
    if code:
        agents.append(MagenticOneCoderAgent("Coder", model_client=client))
        agents.append(CodeExecutorAgent("Executor", code_executor=LocalCommandLineCodeExecutor()))
    
    if not agents:
        raise click.UsageError("At least one capability must be enabled")
    
    return agents

async def run_task(task: str, agents: List[AssistantAgent], hil: bool) -> None:
    client = OpenAIChatCompletionClient(model="gpt-4o")
    m1 = MagenticOne(client=client, hil_mode=hil)
    
    if agents:
        m1._agents = agents
        
    # Show task and agents
    console.rule("[bold blue]Task Started", style="blue")
    console.print(f"[bold cyan]Task:[/bold cyan] {task}")
    console.print("\n[bold cyan]Active Agents:[/bold cyan]")
    for agent in agents:
        console.print(f"• [green]{agent.name}[/green]")
    console.print()
        
    async for message in m1.run_stream(task=task):
        if hasattr(message, 'role'):
            role = message.role.title()
            name = getattr(message, 'name', role)
            content = message.content or ""
            
            # Clean up content
            content = content.strip()
            
            # Create panel title with role if different from name
            title = f"[bold green]{name}[/bold green]"
            if name != role:
                title += f" [dim]({role})[/dim]"
            
            # Create panel with message content
            panel = Panel(
                Text(content, no_wrap=False, justify="left"),
                title=title,
                border_style="blue",
                padding=(1, 2),
                expand=True
            )
            console.print(panel)
        elif hasattr(message, 'type') and message.type == 'TextMessage':
            # Format status messages differently but only if they're really status-like
            content = getattr(message, 'content', str(message))
            if not any(name in content for name in ['Coder', 'FileSurfer', 'WebSurfer', 'Executor']):
                console.print(f"[dim yellow]>>> {content}[/dim yellow]", soft_wrap=True)
        else:
            # Skip printing raw status objects
            pass
    console.rule("[bold blue]Task Completed", style="blue")

@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.argument('task')
@click.option('-w', '--web', is_flag=True, help='Enable web browsing capabilities')
@click.option('--no-files', is_flag=True, help='Disable file system access (enabled by default)')
@click.option('--no-code', is_flag=True, help='Disable code execution (enabled by default)')
@click.option('--no-hil', is_flag=True, help='Disable human-in-the-loop mode (enabled by default)')
def main(task: str, web: bool, no_files: bool, no_code: bool, no_hil: bool) -> None:
    """
    Run a task using MagenticOne with configurable capabilities.
    
    By default, file system access, code execution and human-in-the-loop mode are enabled.
    Web browsing must be explicitly enabled with -w/--web.
    Use --no-files, --no-code, or --no-hil to disable default capabilities.
    """
    setup_openai_key()
    
    client = OpenAIChatCompletionClient(model="gpt-4o")
    agents = create_agents(
        client=client,
        web=web,
        files=not no_files,
        code=not no_code
    )
    
    asyncio.run(run_task(task, agents, not no_hil))

if __name__ == "__main__":
    main()