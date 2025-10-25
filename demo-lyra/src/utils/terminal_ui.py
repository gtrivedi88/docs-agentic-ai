"""
Terminal UI for Lyra demo - beautiful output with Rich library.
"""
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.panel import Panel
from rich.table import Table
import time

console = Console()


def show_demo_banner():
    """Show demo version banner."""
    banner = Panel(
        "[yellow bold]⚠️  DEMONSTRATION VERSION[/yellow bold]\n\n"
        "[white]This demo uses hardcoded data to show Lyra's capabilities.\n"
        "The full version will connect to real Jira, GitHub, Confluence, etc.[/white]",
        title="Lyra Documentation Agent v0.1.0 (DEMO)",
        border_style="yellow"
    )
    console.print(banner)
    console.print()


def show_step(emoji: str, title: str, description: str, duration: float = 0.5):
    """
    Show an agent step with spinner animation.
    
    Args:
        emoji: Emoji to display
        title: Step title
        description: What was accomplished
        duration: How long to show spinner (simulates thinking)
    """
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold]{task.description}[/bold]"),
        console=console,
        transient=True
    ) as progress:
        progress.add_task(f"{emoji} {title}...", total=None)
        time.sleep(duration)
    
    console.print(f"   [green]✓[/green] {description}")


def show_planning_phase():
    """Simulate planning phase."""
    console.print("\n[bold cyan]═══ PLANNING PHASE ═══[/bold cyan]")
    show_step("🔍", "Planning", "Analyzing requirements and determining data sources", 0.3)


def show_jira_exploration(num_tickets: int):
    """Simulate Jira exploration."""
    console.print("\n[bold cyan]═══ JIRA EXPLORATION ═══[/bold cyan]")
    show_step("📊", "Searching Jira", f"Found {num_tickets} tickets for OPSHIFT v2.1", 0.6)
    show_step("🔗", "Following ticket links", "Discovered 2 related tickets through links", 0.4)
    show_step("💬", "Reading comments", "Analyzed 47 comments across all tickets", 0.5)


def show_smart_tool_jira(num_decisions: int):
    """Simulate smart tool distillation for Jira."""
    console.print("\n[bold magenta]═══ SMART TOOL: JIRA DISTILLATION ═══[/bold magenta]")
    show_step("💡", "Distilling decisions", f"Extracted {num_decisions} key decisions from ticket discussions", 0.8)
    show_step("🏷️", "Categorizing", "2 features, 1 bugfix, 1 improvement, 1 internal", 0.3)
    show_step("⚖️", "Filtering", "Removed 1 non-doc-worthy item (internal refactoring)", 0.2)


def show_github_exploration(num_prs: int):
    """Simulate GitHub exploration."""
    console.print("\n[bold cyan]═══ GITHUB EXPLORATION ═══[/bold cyan]")
    show_step("🐙", "Searching PRs", f"Found {num_prs} PRs linked to tickets", 0.6)
    show_step("📝", "Reading PR descriptions", f"Analyzed {num_prs} PR descriptions and changes", 0.5)
    show_step("📊", "Code analysis", "Total: 2,143 lines changed across 7 PRs", 0.4)


def show_smart_tool_github(breaking_changes: int):
    """Simulate smart tool distillation for GitHub."""
    console.print("\n[bold magenta]═══ SMART TOOL: GITHUB DISTILLATION ═══[/bold magenta]")
    show_step("💡", "Analyzing PR impact", "Determined customer-facing impact for each PR", 0.7)
    show_step("⚠️", "Breaking change detection", f"Identified {breaking_changes} breaking change(s)", 0.3)
    show_step("✅", "Doc-worthy filtering", "4 PRs are documentation-worthy, 3 are internal", 0.2)


def show_confluence_exploration(num_pages: int):
    """Simulate Confluence exploration."""
    console.print("\n[bold cyan]═══ CONFLUENCE EXPLORATION ═══[/bold cyan]")
    show_step("📚", "Searching Confluence", f"Found {num_pages} relevant pages for style reference", 0.5)
    show_step("📖", "Reading style guide", "Extracted documentation standards and terminology", 0.4)


def show_synthesis_phase():
    """Simulate synthesis phase."""
    console.print("\n[bold green]═══ SYNTHESIS PHASE ═══[/bold green]")
    show_step("📋", "Gathering knowledge", "Assembled data from all sources", 0.3)
    show_step("✍️", "Generating draft", "Created documentation structure and content", 1.2)
    show_step("🎨", "Applying style", "Formatted according to style guide", 0.4)
    show_step("🔗", "Adding citations", "Included source references (Jira, GitHub, Confluence)", 0.3)


def show_critique_phase(quality_score: float):
    """Simulate critique phase."""
    console.print("\n[bold yellow]═══ QUALITY REVIEW ═══[/bold yellow]")
    show_step("🔍", "Reviewing accuracy", "Verified claims against source data", 0.6)
    show_step("📏", "Checking completeness", "All tickets and PRs covered", 0.4)
    show_step("📝", "Style validation", "Matches style guide requirements", 0.3)
    
    console.print(f"\n   [bold]Quality Score:[/bold] [green]{quality_score}%[/green]")
    
    if quality_score >= 80:
        console.print("   [green]✓[/green] Draft approved for publication")
    else:
        console.print("   [yellow]⚠[/yellow] Draft needs revision")


def show_save_output(output_path: str):
    """Show save operation."""
    console.print("\n[bold blue]═══ SAVING OUTPUT ═══[/bold blue]")
    show_step("💾", "Saving file", f"Saved to: {output_path}", 0.3)


def show_summary_statistics(stats: dict):
    """Show summary statistics table."""
    console.print("\n[bold]═══ EXECUTION SUMMARY ═══[/bold]")
    
    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="white")
    
    table.add_row("Sources Consulted", f"Jira, GitHub, Confluence")
    table.add_row("Jira Tickets", f"{stats.get('jira_tickets', 0)} tickets, {stats.get('jira_comments', 0)} comments")
    table.add_row("GitHub PRs", f"{stats.get('github_prs', 0)} PRs, {stats.get('lines_changed', 0)} lines changed")
    table.add_row("Confluence Pages", f"{stats.get('confluence_pages', 0)} pages")
    table.add_row("Smart Tool Calls", f"{stats.get('smart_tool_calls', 0)} distillations")
    table.add_row("Quality Score", f"{stats.get('quality_score', 0)}%")
    table.add_row("Time Elapsed", f"{stats.get('duration', 0)}s")
    table.add_row("", "")
    table.add_row("Output File", f"[green]{stats.get('output_file', 'N/A')}[/green]")
    
    console.print(table)


def show_preview(content: str, num_lines: int = 15):
    """Show preview of generated content."""
    console.print("\n[bold]═══ PREVIEW ═══[/bold]")
    
    lines = content.split('\n')[:num_lines]
    for line in lines:
        # Syntax highlight markdown
        if line.startswith('# '):
            console.print(f"[bold blue]{line}[/bold blue]")
        elif line.startswith('## '):
            console.print(f"[bold cyan]{line}[/bold cyan]")
        elif line.startswith('### '):
            console.print(f"[bold]{line}[/bold]")
        elif line.startswith('- '):
            console.print(f"[yellow]{line}[/yellow]")
        elif line.startswith('**'):
            console.print(f"[bold]{line}[/bold]")
        else:
            console.print(f"[dim]{line}[/dim]")
    
    console.print("\n   [dim]... (showing first {} lines)[/dim]".format(num_lines))


def show_success(message: str):
    """Show success message."""
    console.print(f"\n✨ [green bold]{message}[/green bold]\n")


def show_error(message: str):
    """Show error message."""
    console.print(f"\n❌ [red bold]Error:[/red bold] {message}\n")


def show_demo_footer():
    """Show demo version reminder."""
    console.print("\n" + "─" * 60)
    console.print("[yellow]DEMO VERSION[/yellow] - Using hardcoded data")
    console.print("[dim]Full version will use real APIs and LLM reasoning[/dim]")
    console.print("─" * 60 + "\n")

