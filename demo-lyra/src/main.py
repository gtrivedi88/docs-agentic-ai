"""
Lyra CLI - DEMONSTRATION VERSION

This is a demo that uses hardcoded data to show Lyra's capabilities.
The full implementation will connect to real APIs and use real LLM reasoning.
"""
import typer
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from demo.demo_agent import demo_agent
from src.utils.terminal_ui import console, show_error

app = typer.Typer(
    name="lyra-demo",
    help="Lyra Documentation Agent (DEMO VERSION)",
    add_completion=False
)


@app.command()
def create_release_notes(
    version: str = typer.Argument(..., help="Release version (e.g., v2.1)"),
    project: str = typer.Option("openshift", help="Project name"),
    show_hardcoded: bool = typer.Option(False, "--show-hardcoded", help="Show what's hardcoded in this demo")
):
    """
    Create release notes for a specific version.
    
    🎬 DEMO VERSION - Uses hardcoded data
    
    Example:
    
        python src/main.py create-release-notes v2.1
        
        python src/main.py create-release-notes v2.1 --show-hardcoded
    """
    try:
        # Show what's hardcoded if requested
        if show_hardcoded:
            demo_agent.show_whats_hardcoded()
            if not typer.confirm("\nContinue with demo?"):
                raise typer.Exit(0)
        
        # Run demo
        output_path = demo_agent.create_release_notes(version, project)
        
        # Offer to open file
        if typer.confirm(f"\nOpen generated file?"):
            import subprocess
            subprocess.run(['xdg-open', str(output_path)])
        
    except Exception as e:
        show_error(f"Demo failed: {e}")
        raise typer.Exit(1)


@app.command()
def info():
    """
    Show information about this demo version.
    """
    from rich.panel import Panel
    
    info_text = """[bold]Lyra Documentation Agent - Demo Version[/bold]

[yellow]This is a demonstration version[/yellow] that shows Lyra's capabilities using hardcoded data.

[bold cyan]What This Demo Shows:[/bold cyan]
  • Multi-source data gathering (Jira, GitHub, Confluence)
  • Smart tool distillation (extracting key decisions from noise)
  • Autonomous exploration (following links, finding related info)
  • Quality documentation synthesis
  • Professional terminal UI with agent reasoning visible

[bold green]What Will Be Real in Full Version:[/bold green]
  • Live API connections to Jira, GitHub, GitLab, Confluence, Slack, Google Docs
  • Real LLM reasoning using Mistral AI
  • Actual smart tool distillation
  • Multiple document types (release notes, help docs, API refs, tutorials)
  • Full CRUD operations (create, update, delete, audit)

[bold blue]Implementation Status:[/bold blue]
  • Complete architecture designed (51 files)
  • Implementation plan ready (5,650 lines)
  • Sprint-based execution plan (6 sprints, 7-9 days)
  • This demo: 1-2 days to build

[bold magenta]Try the Demo:[/bold magenta]
  python src/main.py create-release-notes v2.1 --show-hardcoded

[dim]For full implementation details, see:
  - phase1_implementation_plan.md
  - phase1_incremental_sprints.md
  - working_with_ai_implementation_guide.md[/dim]
"""
    
    panel = Panel(
        info_text,
        title="📋 Demo Information",
        border_style="cyan",
        padding=(1, 2)
    )
    
    console.print(panel)


@app.command()
def version():
    """Show demo version information."""
    console.print("[bold cyan]Lyra Documentation Agent[/bold cyan]")
    console.print("[yellow]Version: 0.1.0-demo[/yellow]")
    console.print("[dim]Full implementation: Phase 1 planned (7-9 days)[/dim]")


if __name__ == "__main__":
    app()

