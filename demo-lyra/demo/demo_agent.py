"""
Simulated agent for Lyra demo.
Uses hardcoded fixture data to demonstrate the complete workflow.
"""
import json
import time
from pathlib import Path
from datetime import datetime
from src.utils.terminal_ui import (
    show_demo_banner,
    show_planning_phase,
    show_jira_exploration,
    show_smart_tool_jira,
    show_github_exploration,
    show_smart_tool_github,
    show_confluence_exploration,
    show_synthesis_phase,
    show_critique_phase,
    show_save_output,
    show_summary_statistics,
    show_preview,
    show_success,
    show_demo_footer,
    console
)


class DemoAgent:
    """
    Demonstration agent that simulates the full Lyra workflow.
    
    This uses hardcoded fixture data to show realistic agent behavior
    without requiring actual API connections or LLM calls.
    """
    
    def __init__(self):
        """Initialize demo agent with fixture data."""
        self.fixtures_dir = Path(__file__).parent / "fixtures"
        self.start_time = None
        
    def create_release_notes(self, version: str, project: str = "openshift") -> Path:
        """
        Simulate creating release notes.
        
        Args:
            version: Release version (e.g., "v2.1")
            project: Project name
            
        Returns:
            Path to generated release notes
        """
        self.start_time = time.time()
        
        # Show demo banner
        show_demo_banner()
        
        # Phase 1: Planning
        show_planning_phase()
        time.sleep(0.5)
        
        # Phase 2: Jira Exploration
        jira_data = self._load_jira_fixtures()
        show_jira_exploration(len(jira_data['tickets']))
        
        # Phase 3: Smart Tool - Jira Distillation
        doc_worthy_count = len([t for t in jira_data['tickets'] if 'customer-facing' in t.get('labels', [])])
        show_smart_tool_jira(doc_worthy_count)
        
        # Phase 4: GitHub Exploration
        github_data = self._load_github_fixtures()
        show_github_exploration(len(github_data['pull_requests']))
        
        # Phase 5: Smart Tool - GitHub Distillation
        breaking_changes = len([pr for pr in github_data['pull_requests'] if 'breaking-change' in pr.get('labels', [])])
        show_smart_tool_github(breaking_changes)
        
        # Phase 6: Confluence Exploration
        confluence_data = self._load_confluence_fixtures()
        show_confluence_exploration(len(confluence_data['pages']))
        
        # Phase 7: Synthesis
        show_synthesis_phase()
        
        # Phase 8: Quality Critique
        quality_score = 87.0
        show_critique_phase(quality_score)
        
        # Phase 9: Save Output
        output_path = self._save_release_notes(version, project)
        show_save_output(str(output_path))
        
        # Show summary statistics
        duration = time.time() - self.start_time
        stats = {
            'jira_tickets': len(jira_data['tickets']),
            'jira_comments': sum(len(t['comments']) for t in jira_data['tickets']),
            'github_prs': len(github_data['pull_requests']),
            'lines_changed': sum(pr['additions'] + pr['deletions'] for pr in github_data['pull_requests']),
            'confluence_pages': len(confluence_data['pages']),
            'smart_tool_calls': 2,  # Jira + GitHub distillation
            'quality_score': int(quality_score),
            'duration': f"{duration:.1f}",
            'output_file': str(output_path)
        }
        show_summary_statistics(stats)
        
        # Show preview
        with open(output_path) as f:
            content = f.read()
        show_preview(content, num_lines=15)
        
        # Success message
        show_success("Release notes created successfully!")
        
        # Show demo footer
        show_demo_footer()
        
        return output_path
    
    def show_whats_hardcoded(self):
        """Show what's hardcoded in this demo."""
        console.print("\n[bold yellow]What's Hardcoded in This Demo:[/bold yellow]\n")
        
        hardcoded = [
            ("Jira Data", "5 sample tickets loaded from demo/fixtures/jira_tickets.json"),
            ("GitHub Data", "7 sample PRs loaded from demo/fixtures/github_prs.json"),
            ("Confluence Data", "2 sample pages loaded from demo/fixtures/confluence_pages.json"),
            ("Release Notes", "Pre-written content from demo/fixtures/expected_output.md"),
            ("Agent Reasoning", "Simulated steps (no real LLM calls)"),
            ("Smart Tool Distillation", "Simulated (no real LLM analysis)")
        ]
        
        for item, description in hardcoded:
            console.print(f"  • [cyan]{item}:[/cyan] {description}")
        
        console.print("\n[bold green]What Will Be Real in Full Version:[/bold green]\n")
        
        real_features = [
            ("API Connections", "Live Jira, GitHub, GitLab, Confluence, Slack, Google Docs"),
            ("LLM Reasoning", "Real Mistral AI for planning and reasoning"),
            ("Smart Tools", "Real LLM distillation of tickets/PRs/pages"),
            ("Autonomous Exploration", "Agent follows links and discovers information"),
            ("Multi-Doc Types", "Release notes, help docs, API refs, tutorials"),
            ("CRUD Operations", "Create, update, delete, audit documentation")
        ]
        
        for item, description in real_features:
            console.print(f"  ✓ [green]{item}:[/green] {description}")
        
        console.print()
    
    def _load_jira_fixtures(self) -> dict:
        """Load hardcoded Jira data."""
        with open(self.fixtures_dir / "jira_tickets.json") as f:
            return json.load(f)
    
    def _load_github_fixtures(self) -> dict:
        """Load hardcoded GitHub data."""
        with open(self.fixtures_dir / "github_prs.json") as f:
            return json.load(f)
    
    def _load_confluence_fixtures(self) -> dict:
        """Load hardcoded Confluence data."""
        with open(self.fixtures_dir / "confluence_pages.json") as f:
            return json.load(f)
    
    def _save_release_notes(self, version: str, project: str) -> Path:
        """
        Save the pre-written release notes.
        
        Args:
            version: Release version
            project: Project name
            
        Returns:
            Path to saved file
        """
        # Load pre-written output
        with open(self.fixtures_dir / "expected_output.md") as f:
            content = f.read()
        
        # Create output directory
        output_dir = Path("demo/outputs")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Save file
        output_path = output_dir / f"{project}_{version}_release_notes.md"
        with open(output_path, 'w') as f:
            f.write(content)
        
        return output_path


# Global demo agent instance
demo_agent = DemoAgent()

