import typer
from rich.console import Console
from rich.markdown import Markdown

from ai_agent.agent.graph import run_agent

app = typer.Typer(add_completion=False, help="LangGraph support agent with RAG + tools")
console = Console()


@app.command()
def ask(question: str = typer.Argument(..., help="User question for the agent")):
    """Ask the support agent a question."""

    console.print("[bold cyan]Running agent...[/bold cyan]")
    answer = run_agent(question)
    console.print(Markdown(answer))


if __name__ == "__main__":
    app()
