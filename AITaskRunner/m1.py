# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "click",
#     "autogen-agentchat",
#     "autogen-ext[magentic-one-base,openai]",
# ]
# [project.optional-dependencies]
# web = [
#     "autogen-ext[web]",
#     "playwright",
# ]
# ///

import asyncio
import os
from typing import List

import click
from autogen_agentchat.agents import ChatAgent, CodeExecutorAgent
from autogen_agentchat.ui import Console
from autogen_ext.agents.file_surfer import FileSurfer
from autogen_ext.agents.magentic_one import MagenticOneCoderAgent
from autogen_ext.agents.web_surfer import MultimodalWebSurfer
from autogen_ext.code_executors.local import LocalCommandLineCodeExecutor
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.teams.magentic_one import MagenticOne

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
                 files: bool = True, code: bool = True) -> List[ChatAgent]:
    agents: List[ChatAgent] = []
    
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

async def run_task(task: str, agents: List[ChatAgent], hil: bool) -> None:
    client = OpenAIChatCompletionClient(model="gpt-4o")
    m1 = MagenticOne(client=client, hil_mode=hil)
    
    if agents:
        m1._agents = agents
        
    result = await Console(m1.run_stream(task=task))
    click.echo(result)

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