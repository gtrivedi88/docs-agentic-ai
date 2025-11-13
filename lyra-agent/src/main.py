"""
Lyra CLI - Sprint 1 version (create release-notes only).
"""
import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel

from src.operations.doc_creator import doc_creator
from src.config.settings import settings
from src.utils.logger import logger

app = typer.Typer(
    name="lyra",
    help="Lyra - Autonomous Documentation Agent (Sprint 1)",
    add_completion=False
)
console = Console()


@app.command()
def create_release_notes(
    version: str = typer.Argument(..., help="Release version (e.g., v2.1)"),
    project: str = typer.Option(settings.project_name, help="Project name"),
):
    """
    Create release notes for a specific version.
    
    Example:
        lyra create-release-notes v2.1 --project=developerhub
    """
    console.print(Panel(
        f"[bold blue]Creating release notes[/bold blue]\n"
        f"Version: {version}\n"
        f"Project: {project}",
        title="Lyra Documentation Agent (Sprint 1)"
    ))
    
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Generating release notes...", total=None)
            
            draft = doc_creator.create_release_notes(version, project)
            
            progress.update(task, completed=True)
        
        console.print("\n[green]✓ Release notes created successfully![/green]")
        console.print(f"[dim]Title: {draft.title}[/dim]")
        console.print(f"[dim]Confidence: {draft.confidence_score:.0%}[/dim]")
        console.print(f"[dim]Sources: {', '.join(draft.metadata.get('sources_used', []))}[/dim]")
        
        # Show preview
        lines = draft.content.split('\n')[:10]
        console.print("\n[bold]Preview:[/bold]")
        for line in lines:
            console.print(f"  {line}")
        console.print("  [dim]...[/dim]")
        
    except Exception as e:
        console.print(f"\n[red]✗ Failed to create release notes: {e}[/red]")
        logger.exception("Release notes creation failed")
        raise typer.Exit(1)


@app.command()
def version():
    """Show Lyra version."""
    console.print("Lyra v0.1.0 (Sprint 1)")


if __name__ == "__main__":
    app()

