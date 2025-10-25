# Lyra Phase 1: Incremental Sprint Implementation
## Building Complexity Management Through Vertical Slices

**Version**: 1.0  
**Approach**: Incremental, sprint-based development  
**Tech Stack**: Python 3.10+, LangChain, Mistral API, LangGraph  
**Philosophy**: Build working end-to-end first, then add capabilities incrementally

---

## Table of Contents
1. [Why Incremental Sprints?](#why-incremental-sprints)
2. [Sprint Overview](#sprint-overview)
3. [Sprint 1: Core Release Notes (FOUNDATION)](#sprint-1-core-release-notes)
4. [Sprint 2: Add Confluence Intelligence](#sprint-2-add-confluence-intelligence)
5. [Sprint 3: Add Audit Capability](#sprint-3-add-audit-capability)
6. [Sprint 4: Add Help Documentation](#sprint-4-add-help-documentation)
7. [Sprint 5: Add Remaining Data Sources](#sprint-5-add-remaining-data-sources)
8. [Sprint 6: Complete CRUD Operations](#sprint-6-complete-crud-operations)

---

## Why Incremental Sprints?

### The Integration Hell Problem

**Building everything at once** creates:
- **36+ integration points** to debug simultaneously
- **Agent cognitive overload** (20+ tools to choose from)
- **Un-testable system** (can't isolate failures)
- **Delayed value** (no working demo until everything is done)
- **High risk** (if one piece fails, everything fails)

### The Vertical Slice Solution

**Building incrementally** provides:
- ✅ **Working demo in 2 days** (Sprint 1)
- ✅ **Testable at each step** (isolate failures)
- ✅ **Manageable complexity** (2-4 tools at a time)
- ✅ **Proven architecture** (before investing in everything)
- ✅ **Low risk** (each sprint builds on working foundation)

### Key Principle

> Each sprint delivers a **working, deployable system**. Not a prototype, not a proof-of-concept, but a system you can actually use.

---

## Sprint Overview

| Sprint | Duration | Goal | Tools Added | Operations Added | Value Delivered |
|--------|----------|------|-------------|------------------|-----------------|
| **Sprint 1** | 2 days | Release notes work | Jira, GitHub | create release-notes | ✅ Working e2e system |
| **Sprint 2** | 1 day | Smarter docs | + Confluence | - | ✅ Style consistency |
| **Sprint 3** | 1 day | Find outdated docs | - | + audit | ✅ Doc maintenance |
| **Sprint 4** | 1 day | Multiple doc types | - | create help-doc | ✅ Generalization |
| **Sprint 5** | 1-2 days | More sources | + GitLab, Slack, GDocs | - | ✅ Comprehensive data |
| **Sprint 6** | 1 day | Full CRUD | - | + update, delete | ✅ Complete lifecycle |

**Total**: 7-9 days to fully functional system

---

## Sprint 1: Core Release Notes (FOUNDATION)

**Duration**: 2 days  
**Goal**: `lyra create release-notes v2.1 openshift` produces working release notes  
**Success Criteria**: End-to-end working system with 2 data sources

### Why This Sprint is Critical

This sprint **proves the entire architecture works**:
- ✅ Agent can reason with tools
- ✅ Smart tools distillation works
- ✅ Synthesis produces quality docs
- ✅ CLI works
- ✅ LangGraph orchestration works

**If Sprint 1 fails**, you know immediately and can fix architecture.  
**If Sprint 1 succeeds**, everything else is additive.

### What to Implement

#### Phase 0: Scaffolding (Same as full plan)
- Directory structure
- `pyproject.toml` with dependencies
- `.env.example`
- `src/config/settings.py`
- `src/utils/logger.py`
- `src/schemas/data_models.py` (all models, we'll use them later)

#### Tools Layer: Jira + GitHub ONLY

**File**: `src/tools/base_tool.py`
```python
"""Base tool with caching - COMPLETE implementation from full plan"""
# [Use exact code from phase1_implementation_plan.md]
```

**File**: `src/tools/jira_tool.py`
```python
"""Jira tool - COMPLETE implementation from full plan"""
# [Use exact code from phase1_implementation_plan.md]
# Includes: search_tickets, get_ticket_details, get_tickets_for_release, follow_linked_issues
```

**File**: `src/tools/github_tool.py`
```python
"""GitHub tool - COMPLETE implementation from full plan"""
# [Use exact code from phase1_implementation_plan.md]
# Includes: search_prs, get_pr_details, find_prs_for_ticket, check_file_exists
```

**File**: `src/tools/smart_tools.py` - **SIMPLIFIED for Sprint 1**
```python
"""
Smart tools - Sprint 1 version (Jira + GitHub only)
"""
from typing import Dict, Any, List
from langchain.tools import tool
from langchain_mistralai import ChatMistralAI
import json
from src.tools.jira_tool import jira_tool
from src.tools.github_tool import github_tool
from src.config.settings import settings
from src.utils.logger import logger


class SmartToolOrchestrator:
    """Smart tools for Jira and GitHub only (Sprint 1)."""
    
    def __init__(self):
        self.llm = ChatMistralAI(
            model=settings.mistral_model,
            api_key=settings.mistral_api_key,
            temperature=0
        )
        logger.info("Smart Tool Orchestrator initialized (Sprint 1: Jira + GitHub)")
    
    def distill_ticket_decision(self, ticket_id: str) -> Dict[str, Any]:
        """Distill Jira ticket into key decision."""
        # [Use exact implementation from full plan]
        ticket = jira_tool.get_ticket_details(ticket_id)
        
        comments_text = "\n\n".join([
            f"Comment by {c.author} on {c.created}:\n{c.body}"
            for c in ticket.comments
        ])
        
        prompt = f"""You are analyzing a Jira ticket to extract the key technical decision.

Ticket: {ticket.key} - {ticket.summary}

Description:
{ticket.description}

Comments:
{comments_text}

Task: Extract the FINAL technical decision made in this ticket.

Return ONLY a JSON object with:
{{
    "decision": "One clear sentence describing what was decided",
    "rationale": "Why this decision was made",
    "decided_by": "Who made or approved the decision",
    "is_doc_worthy": true/false (is this important for user-facing documentation?),
    "category": "feature|bugfix|improvement|internal",
    "confidence": 0.0-1.0 (how clear is this decision?)
}}

If no clear decision was made, set confidence to 0.0.
"""
        
        try:
            response = self.llm.invoke(prompt)
            result = json.loads(response.content)
            
            result["source_ticket"] = ticket_id
            result["ticket_status"] = ticket.status
            result["fix_versions"] = ticket.fix_versions
            
            logger.debug(f"Distilled {ticket_id}: {result['decision'][:50]}...")
            return result
            
        except Exception as e:
            logger.error(f"Failed to distill ticket {ticket_id}: {e}")
            return {
                "decision": f"Error processing ticket {ticket_id}",
                "confidence": 0.0,
                "is_doc_worthy": False
            }
    
    def distill_pr_impact(self, repo_name: str, pr_number: int) -> Dict[str, Any]:
        """Distill GitHub PR into user impact."""
        # [Use exact implementation from full plan]
        pr = github_tool.get_pr_details(repo_name, pr_number)
        
        prompt = f"""You are analyzing a GitHub Pull Request to determine its impact.

PR #{pr.number}: {pr.title}

Description:
{pr.body or 'No description'}

Files Changed: {pr.files_changed}
Additions: {pr.additions}
Deletions: {pr.deletions}
Diff Summary: {pr.diff_summary}

Linked Issues: {', '.join(pr.linked_issues)}

Task: Determine the customer-facing impact of this PR.

Return ONLY a JSON object with:
{{
    "impact": "One sentence describing what changed for users",
    "impact_type": "feature|bugfix|performance|security|breaking_change|internal",
    "is_breaking": true/false,
    "is_doc_worthy": true/false,
    "technical_details": "Brief technical summary",
    "confidence": 0.0-1.0
}}

If this is purely internal/refactoring with no user impact, set is_doc_worthy to false.
"""
        
        try:
            response = self.llm.invoke(prompt)
            result = json.loads(response.content)
            
            result["source_pr"] = pr_number
            result["repo"] = repo_name
            result["merged_at"] = str(pr.merged_at) if pr.merged_at else None
            result["linked_issues"] = pr.linked_issues
            
            logger.debug(f"Distilled PR #{pr_number}: {result['impact'][:50]}...")
            return result
            
        except Exception as e:
            logger.error(f"Failed to distill PR {pr_number}: {e}")
            return {
                "impact": f"Error processing PR {pr_number}",
                "confidence": 0.0,
                "is_doc_worthy": False
            }
    
    def get_release_knowledge(self, release_version: str, project_name: str) -> Dict[str, Any]:
        """Smart aggregator for release (Jira + GitHub only)."""
        # [Use exact implementation from full plan]
        logger.info(f"Gathering smart knowledge for {release_version}")
        
        tickets = jira_tool.get_tickets_for_release(release_version)
        
        features = []
        bugfixes = []
        improvements = []
        breaking_changes = []
        
        for ticket in tickets:
            distilled = self.distill_ticket_decision(ticket.key)
            
            if not distilled.get("is_doc_worthy", False):
                continue
            
            prs = github_tool.find_prs_for_ticket(ticket.key)
            pr_impacts = []
            for pr in prs[:3]:
                impact = self.distill_pr_impact(pr.url.split('/')[-4] + '/' + pr.url.split('/')[-3], pr.number)
                if impact.get("is_doc_worthy"):
                    pr_impacts.append(impact)
            
            entry = {
                "ticket": ticket.key,
                "decision": distilled["decision"],
                "rationale": distilled["rationale"],
                "pr_impacts": pr_impacts,
                "confidence": distilled["confidence"]
            }
            
            category = distilled.get("category", "improvement")
            if category == "feature":
                features.append(entry)
            elif category == "bugfix":
                bugfixes.append(entry)
            elif category == "improvement":
                improvements.append(entry)
            
            if any(pr.get("is_breaking") for pr in pr_impacts):
                breaking_changes.append(entry)
        
        return {
            "release_version": release_version,
            "project": project_name,
            "features": features,
            "bugfixes": bugfixes,
            "improvements": improvements,
            "breaking_changes": breaking_changes,
            "total_tickets": len(tickets),
            "doc_worthy_items": len(features) + len(bugfixes) + len(improvements)
        }


# Global orchestrator
smart_orchestrator = SmartToolOrchestrator()


# LangChain tool wrappers
@tool
def get_smart_release_knowledge(release_version: str, project_name: str) -> str:
    """
    Get distilled release knowledge (Sprint 1: Jira + GitHub only).
    """
    knowledge = smart_orchestrator.get_release_knowledge(release_version, project_name)
    return json.dumps(knowledge, indent=2, default=str)


@tool
def get_ticket_decision_summary(ticket_id: str) -> str:
    """Get clean summary of Jira ticket decision."""
    summary = smart_orchestrator.distill_ticket_decision(ticket_id)
    return json.dumps(summary, indent=2)


@tool
def get_pr_impact_summary(repo_name: str, pr_number: int) -> str:
    """Get clean summary of PR impact."""
    summary = smart_orchestrator.distill_pr_impact(repo_name, pr_number)
    return json.dumps(summary, indent=2)
```

**File**: `src/tools/tool_registry.py` - **SIMPLIFIED for Sprint 1**
```python
"""
Tool registry - Sprint 1 version (Jira + GitHub only)
"""
from typing import List
from langchain.tools import Tool
from src.tools.jira_tool import (
    search_jira_tickets,
    get_jira_ticket,
    get_jira_release_tickets,
    get_linked_jira_tickets
)
from src.tools.github_tool import (
    search_github_prs,
    get_github_pr,
    find_github_prs_for_ticket,
    check_github_file_exists
)
from src.tools.smart_tools import (
    get_smart_release_knowledge,
    get_ticket_decision_summary,
    get_pr_impact_summary
)
from src.utils.logger import logger


def get_all_tools() -> List[Tool]:
    """
    Get all tools - Sprint 1 version.
    
    Only Jira and GitHub tools included.
    """
    tools = [
        # Smart tools (preferred)
        get_smart_release_knowledge,
        get_ticket_decision_summary,
        get_pr_impact_summary,
        
        # Raw tools (fallback)
        search_jira_tickets,
        get_jira_ticket,
        get_jira_release_tickets,
        get_linked_jira_tickets,
        search_github_prs,
        get_github_pr,
        find_github_prs_for_ticket,
        check_github_file_exists,
    ]
    
    logger.info(f"Loaded {len(tools)} tools (Sprint 1: Jira + GitHub only)")
    return tools
```

#### Agent Core: Complete (All Nodes)

**All agent files from full plan**:
- `src/schemas/agent_state.py` - Complete
- `src/agents/node_utils.py` - Complete
- `src/agents/planner_node.py` - Complete
- `src/agents/executor_node.py` - Complete
- `src/agents/synthesizer_node.py` - Complete
- `src/agents/critic_node.py` - Complete
- `src/agents/controller.py` - Complete

**Why implement full agent now?**
- Proves architecture works
- Won't need to change for future sprints
- Each node is modular and testable

#### Knowledge Service: Basic Version

**File**: `src/services/vector_store.py` - Complete (from full plan)

**File**: `src/services/knowledge_service.py` - **SIMPLIFIED for Sprint 1**
```python
"""
Knowledge service - Sprint 1 version.
Simplified to just handle existing docs for style examples.
"""
from typing import List, Dict, Any, Optional
from datetime import datetime
from src.services.vector_store import VectorStoreService
from src.utils.logger import logger
from pathlib import Path


class KnowledgeService:
    """Simplified knowledge service for Sprint 1."""
    
    def __init__(self):
        self.vector_store = VectorStoreService()
        logger.info("Knowledge Service initialized (Sprint 1)")
    
    def index_existing_docs(self, docs_directory: str = "./data/existing_docs"):
        """Index existing documentation for style examples."""
        docs_path = Path(docs_directory)
        if not docs_path.exists():
            logger.warning(f"Docs directory not found: {docs_directory}")
            return
        
        documents = []
        for doc_file in docs_path.rglob("*.md"):
            content = doc_file.read_text()
            documents.append({
                'content': content,
                'metadata': {
                    'filename': doc_file.name,
                    'path': str(doc_file),
                    'indexed_at': datetime.now().isoformat()
                }
            })
        
        if documents:
            self.vector_store.index_documents(documents, "existing_docs")
            logger.info(f"Indexed {len(documents)} existing documents")
    
    def get_style_examples(self, doc_type: str, n_examples: int = 3) -> List[str]:
        """Get style examples for a document type."""
        query = f"{doc_type} documentation example"
        results = self.vector_store.search(
            query=query,
            source_types=["existing_docs"],
            k=n_examples
        )
        
        return [r['content'] for r in results]
```

#### Operations: Release Notes Only

**File**: `src/operations/doc_creator.py` - **SIMPLIFIED for Sprint 1**
```python
"""
Document creator - Sprint 1 version (release notes only).
"""
from pathlib import Path
from src.agents.controller import create_lyra_agent
from src.schemas.data_models import DocDraft
from src.config.settings import settings
from src.utils.logger import logger
from src.utils.metrics import AgentMetrics


class DocumentCreator:
    """Creates release notes using the agent."""
    
    def __init__(self):
        self.agent = create_lyra_agent()
        logger.info("Document Creator initialized (Sprint 1: release notes only)")
    
    def create_release_notes(self, release_version: str, project_name: str) -> DocDraft:
        """Create release notes for a specific version."""
        logger.info(f"Creating release notes for {project_name} {release_version}")
        
        metrics = AgentMetrics()
        
        initial_state = {
            "user_goal": f"Create comprehensive release notes for {project_name} version {release_version}",
            "doc_type": "release_notes",
            "release_version": release_version,
            "topic": None,
            "project_name": project_name,
            "messages": [],
            "knowledge_bundle": [],
            "sources_explored": [],
            "draft": None,
            "revision_count": 0,
            "critique_notes": "",
            "quality_score": 0.0,
            "approved": False,
            "next_action": "start",
            "iterations": 0,
            "max_iterations": settings.max_iterations
        }
        
        try:
            final_state = self.agent.invoke(initial_state)
            metrics.finish()
            metrics.iterations = final_state.get('iterations', 0)
            metrics.log_summary()
            
            draft = final_state.get('draft')
            if draft:
                self._save_draft(draft, project_name, "release_notes", release_version)
                return draft
            else:
                raise Exception("Agent failed to generate draft")
                
        except Exception as e:
            logger.error(f"Failed to create release notes: {e}")
            raise
    
    def _save_draft(self, draft: DocDraft, project_name: str, doc_type: str, identifier: str):
        """Save draft to output directory."""
        output_dir = Path(f"./outputs/generated_docs/{project_name}/{doc_type}")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        filename = f"{identifier}.md"
        filepath = output_dir / filename
        
        with open(filepath, 'w') as f:
            f.write(draft.content)
        
        logger.info(f"Draft saved to: {filepath}")


# Global instance
doc_creator = DocumentCreator()
```

#### CLI: Create Command Only

**File**: `src/main.py` - **SIMPLIFIED for Sprint 1**
```python
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
        lyra create-release-notes v2.1 --project=openshift
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
```

#### Templates: Release Notes Only

**File**: `data/templates/release_notes.md`
```markdown
# Release Notes: {project_name} {version}

**Release Date**: {release_date}

## Overview

{brief_overview}

## New Features

### Feature Name
- **Description**: What this feature does
- **Jira**: [TICKET-123]
- **Pull Request**: [#456]

{more_features}

## Improvements

- **Performance**: {performance_improvements}
- **Security**: {security_improvements}

## Bug Fixes

{bug_fixes_list}

## Breaking Changes

⚠️ **IMPORTANT**: This release contains breaking changes.

{breaking_changes_list}

## Contributors

{contributors_list}
```

### Sprint 1 Testing

**File**: `tests/test_sprint1.py`
```python
"""
Sprint 1 integration tests.
"""
import pytest
from src.operations.doc_creator import doc_creator


def test_create_release_notes_basic():
    """Test basic release notes creation."""
    # This will require real API credentials or mocking
    # For now, just test the structure
    assert doc_creator is not None


def test_tools_loaded():
    """Test that Sprint 1 tools are loaded."""
    from src.tools.tool_registry import get_all_tools
    tools = get_all_tools()
    
    # Should have exactly 11 tools (3 smart + 8 raw for Jira/GitHub)
    assert len(tools) == 11
    
    # Check smart tools are present
    tool_names = [t.name for t in tools]
    assert "get_smart_release_knowledge" in tool_names
    assert "get_ticket_decision_summary" in tool_names
    assert "get_pr_impact_summary" in tool_names


def test_agent_graph_creates():
    """Test that agent graph can be created."""
    from src.agents.controller import create_lyra_agent
    graph = create_lyra_agent()
    assert graph is not None
```

### Sprint 1 Success Criteria

✅ **Can run**: `lyra create-release-notes v2.1 --project=openshift`  
✅ **Agent uses**: Jira and GitHub tools  
✅ **Smart tools work**: Distills decisions and PR impacts  
✅ **Output**: Readable markdown release notes  
✅ **Citations**: Include source tickets and PRs  
✅ **No errors**: Clean execution end-to-end  

### Sprint 1 Deliverables

- [ ] Working CLI command
- [ ] 2 data source integrations (Jira, GitHub)
- [ ] Complete agent (all 4 nodes)
- [ ] Smart tool distillation
- [ ] Generated release notes file
- [ ] Basic tests pass

**After Sprint 1**: You have a **working, deployable system** that generates release notes. Everything else builds on this.

---

## Sprint 2: Add Confluence Intelligence

**Duration**: 1 day  
**Goal**: Release notes now use existing docs for style consistency  
**What Changes**: Add 1 new tool, update planner

### Why This Sprint

Proves the system can **add new data sources** without breaking existing functionality.

### What to Add

#### New Tool: Confluence

**File**: `src/tools/confluence_tool.py`
```python
"""Confluence tool - COMPLETE from full plan"""
# [Use exact code from phase1_implementation_plan.md]
```

#### Update Smart Tools

**File**: `src/tools/smart_tools.py` - ADD Confluence support
```python
# Add to SmartToolOrchestrator class:

def distill_confluence_key_points(self, page_id: str) -> Dict[str, Any]:
    """Distill Confluence page into key points."""
    from src.tools.confluence_tool import confluence_tool
    
    page = confluence_tool.get_page_details(page_id)
    
    prompt = f"""Extract key points from this Confluence page.

Title: {page.title}

Content:
{page.content[:2000]}...

Task: Extract the most important information.

Return JSON:
{{
    "key_points": ["point 1", "point 2", ...],
    "doc_style": "formal|casual|technical",
    "terminology": ["term1", "term2", ...],
    "confidence": 0.0-1.0
}}
"""
    
    response = self.llm.invoke(prompt)
    return json.loads(response.content)


# Add LangChain tool wrapper:
@tool
def get_confluence_key_points(page_id: str) -> str:
    """Get key points from Confluence page."""
    summary = smart_orchestrator.distill_confluence_key_points(page_id)
    return json.dumps(summary, indent=2)
```

#### Update Tool Registry

**File**: `src/tools/tool_registry.py` - ADD Confluence tools
```python
from src.tools.confluence_tool import (
    search_confluence_pages,
    get_confluence_page
)
from src.tools.smart_tools import (
    get_smart_release_knowledge,
    get_ticket_decision_summary,
    get_pr_impact_summary,
    get_confluence_key_points  # NEW
)

def get_all_tools() -> List[Tool]:
    tools = [
        # Smart tools
        get_smart_release_knowledge,
        get_ticket_decision_summary,
        get_pr_impact_summary,
        get_confluence_key_points,  # NEW
        
        # Raw tools
        search_jira_tickets,
        # ... existing Jira/GitHub tools ...
        search_confluence_pages,  # NEW
        get_confluence_page,  # NEW
    ]
    
    logger.info(f"Loaded {len(tools)} tools (Sprint 2: + Confluence)")
    return tools
```

#### Update Knowledge Service

**File**: `src/services/knowledge_service.py` - ADD Confluence indexing
```python
def index_confluence_pages(self, space_key: Optional[str] = None):
    """Index Confluence pages for search."""
    from src.tools.confluence_tool import confluence_tool
    
    if space_key:
        pages = confluence_tool.get_pages_in_space(space_key)
    else:
        # Index recent pages
        pages = confluence_tool.search_pages("", max_results=50)
    
    documents = []
    for page in pages:
        documents.append({
            'content': page.content,
            'metadata': {
                'page_id': page.id,
                'title': page.title,
                'url': str(page.url),
                'indexed_at': datetime.now().isoformat()
            }
        })
    
    if documents:
        self.vector_store.index_documents(documents, "confluence")
        logger.info(f"Indexed {len(documents)} Confluence pages")
```

### Sprint 2 Testing

```python
def test_confluence_tool_added():
    """Test Confluence tools are now available."""
    from src.tools.tool_registry import get_all_tools
    tools = get_all_tools()
    tool_names = [t.name for t in tools]
    
    assert "search_confluence_pages" in tool_names
    assert "get_confluence_key_points" in tool_names


def test_release_notes_with_confluence():
    """Test that release notes can now use Confluence."""
    # Agent should be able to search Confluence for style
    # This proves integration without breaking Sprint 1
    pass
```

### Sprint 2 Success Criteria

✅ **Sprint 1 still works**: Can still generate release notes  
✅ **Confluence accessible**: Agent can search Confluence pages  
✅ **Style consistency**: Release notes match existing doc style  
✅ **No regression**: All Sprint 1 tests still pass  

---

## Sprint 3: Add Audit Capability

**Duration**: 1 day  
**Goal**: `lyra audit-docs ./docs` finds outdated documentation  
**What Changes**: Add new operation, new CLI command

### Why This Sprint

Proves the system supports **multiple operations**, not just creation. Tests architecture flexibility.

### What to Add

#### New Operation: Auditor

**File**: `src/operations/doc_auditor.py`
```python
"""Document auditor - COMPLETE from full plan"""
# [Use exact code from phase1_implementation_plan.md]
# Reuses GitHub tool to check if endpoints exist
```

#### Update CLI

**File**: `src/main.py` - ADD audit command
```python
from src.operations.doc_auditor import doc_auditor

@app.command()
def audit(
    docs_dir: str = typer.Argument(..., help="Directory containing documentation"),
    project: str = typer.Option(settings.project_name, help="Project name"),
):
    """
    Audit documentation for outdated content.
    
    Example:
        lyra audit ./docs --project=openshift
    """
    console.print(Panel(
        f"[bold blue]Auditing documentation[/bold blue]\n"
        f"Directory: {docs_dir}\n"
        f"Project: {project}",
        title="Lyra Documentation Agent"
    ))
    
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Auditing documents...", total=None)
            results = doc_auditor.audit_documentation(docs_dir, project)
            progress.update(task, completed=True)
        
        # Display summary
        current = len([r for r in results if r.status == "current"])
        outdated = len([r for r in results if r.status == "outdated"])
        deprecated = len([r for r in results if r.status == "deprecated"])
        
        console.print(f"\n[bold]Audit Results:[/bold]")
        console.print(f"  Total Documents: {len(results)}")
        console.print(f"  [green]Current: {current}[/green]")
        console.print(f"  [yellow]Outdated: {outdated}[/yellow]")
        console.print(f"  [red]Deprecated: {deprecated}[/red]")
        
        if outdated > 0 or deprecated > 0:
            console.print(f"\n[dim]Full report: ./outputs/reports/{project}_audit_report.md[/dim]")
        
    except Exception as e:
        console.print(f"\n[red]✗ Audit failed: {e}[/red]")
        logger.exception("Documentation audit failed")
        raise typer.Exit(1)
```

### Sprint 3 Success Criteria

✅ **New command works**: `lyra audit ./docs`  
✅ **Finds outdated docs**: Correctly identifies deprecated content  
✅ **Generates report**: Creates audit report file  
✅ **Sprint 1 + 2 still work**: No regressions  

---

## Sprint 4: Add Help Documentation

**Duration**: 1 day  
**Goal**: `lyra create-help-doc "OAuth" openshift` works  
**What Changes**: Add help doc template, update synthesizer

### Why This Sprint

Proves the system can handle **multiple document types**. Tests generalization.

### What to Add

#### New Template

**File**: `data/templates/help_doc.md`
```markdown
# {topic_title}

## Overview

{brief_description}

## Prerequisites

- {prerequisite_1}
- {prerequisite_2}

## Quick Start

{quick_start_steps}

## Detailed Guide

### Step 1: {step_name}

{step_description}

## Configuration

{configuration_details}

## Troubleshooting

{troubleshooting}

## Related Documentation

- {related_links}
```

#### Update Document Creator

**File**: `src/operations/doc_creator.py` - ADD help doc method
```python
def create_help_doc(self, topic: str, project_name: str) -> DocDraft:
    """Create help documentation for a specific topic."""
    logger.info(f"Creating help documentation for: {topic}")
    
    initial_state = {
        "user_goal": f"Create comprehensive help documentation for {topic} in {project_name}",
        "doc_type": "help_doc",
        "release_version": None,
        "topic": topic,
        "project_name": project_name,
        "messages": [],
        "knowledge_bundle": [],
        "sources_explored": [],
        "draft": None,
        "revision_count": 0,
        "critique_notes": "",
        "quality_score": 0.0,
        "approved": False,
        "next_action": "start",
        "iterations": 0,
        "max_iterations": settings.max_iterations
    }
    
    try:
        final_state = self.agent.invoke(initial_state)
        draft = final_state.get('draft')
        if draft:
            self._save_draft(draft, project_name, "help_doc", topic.replace(' ', '_'))
            return draft
        else:
            raise Exception("Agent failed to generate draft")
    except Exception as e:
        logger.error(f"Failed to create help doc: {e}")
        raise
```

#### Update CLI

**File**: `src/main.py` - ADD help-doc command
```python
@app.command()
def create_help_doc(
    topic: str = typer.Argument(..., help="Topic for help documentation"),
    project: str = typer.Option(settings.project_name, help="Project name"),
):
    """
    Create help documentation for a topic.
    
    Example:
        lyra create-help-doc "OAuth Authentication" --project=openshift
    """
    console.print(Panel(
        f"[bold blue]Creating help documentation[/bold blue]\n"
        f"Topic: {topic}\n"
        f"Project: {project}",
        title="Lyra Documentation Agent"
    ))
    
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Generating help doc...", total=None)
            draft = doc_creator.create_help_doc(topic, project)
            progress.update(task, completed=True)
        
        console.print("\n[green]✓ Help documentation created![/green]")
        console.print(f"[dim]Title: {draft.title}[/dim]")
        
    except Exception as e:
        console.print(f"\n[red]✗ Failed: {e}[/red]")
        raise typer.Exit(1)
```

### Sprint 4 Success Criteria

✅ **Help docs work**: Can create help documentation  
✅ **Different format**: Help docs different from release notes  
✅ **Same agent**: Uses same agent core (no changes needed)  
✅ **All previous sprints work**: No regressions  

---

## Sprint 5: Add Remaining Data Sources

**Duration**: 1-2 days  
**Goal**: Agent can access GitLab, Slack, Google Docs  
**What Changes**: Add 3 tools, update incrementally

### Why This Sprint

Adds **comprehensive data coverage**. But done last because not critical for core functionality.

### Strategy: Add One at a Time

**Day 1 Morning**: Add GitLab
- `src/tools/gitlab_tool.py`
- Update tool registry
- Test with release notes
- Verify no issues

**Day 1 Afternoon**: Add Slack
- `src/tools/slack_tool.py`
- Update tool registry
- Test with release notes
- Verify no issues

**Day 2**: Add Google Docs
- `src/tools/gdocs_tool.py`
- Update tool registry
- Test with release notes
- Verify no issues

### What to Add

**Files** (from full plan):
- `src/tools/gitlab_tool.py` - Complete
- `src/tools/slack_tool.py` - Complete
- `src/tools/gdocs_tool.py` - Complete

**Tool Registry Updates** - Add incrementally:
```python
# After GitLab works:
from src.tools.gitlab_tool import search_gitlab_merge_requests

# After Slack works:
from src.tools.slack_tool import search_slack_messages

# After Google Docs works:
from src.tools.gdocs_tool import search_google_docs, get_google_doc
```

### Sprint 5 Success Criteria

✅ **3 new sources work**: GitLab, Slack, Google Docs accessible  
✅ **Agent uses them**: Release notes can include Slack decisions  
✅ **Not overwhelming**: Agent still picks right tools  
✅ **All previous sprints work**: No regressions  

---

## Sprint 6: Complete CRUD Operations

**Duration**: 1 day  
**Goal**: Full create, update, delete capabilities  
**What Changes**: Add update and delete operations

### Why This Sprint

Completes the **full documentation lifecycle**. Proves system handles all operations.

### What to Add

#### Update Operation

**File**: `src/operations/doc_updater.py`
```python
"""Document updater - COMPLETE from full plan"""
# [Use exact code from phase1_implementation_plan.md]
```

#### Delete Operation

**File**: `src/operations/doc_deleter.py`
```python
"""Document deleter - COMPLETE from full plan"""
# [Use exact code from phase1_implementation_plan.md]
```

#### Update CLI

**File**: `src/main.py` - ADD update and delete commands
```python
from src.operations.doc_updater import doc_updater
from src.operations.doc_deleter import doc_deleter

@app.command()
def update(
    doc_path: str = typer.Argument(..., help="Path to document"),
    project: str = typer.Option(settings.project_name, help="Project name"),
    reason: Optional[str] = typer.Option(None, help="Reason for update"),
):
    """Update existing documentation."""
    # [Implementation from full plan]


@app.command()
def delete(
    doc_path: str = typer.Argument(..., help="Path to document"),
    project: str = typer.Option(settings.project_name, help="Project name"),
    reason: str = typer.Option(..., help="Reason for deletion"),
    hard: bool = typer.Option(False, help="Permanently delete"),
):
    """Delete or deprecate documentation."""
    # [Implementation from full plan]
```

### Sprint 6 Success Criteria

✅ **Update works**: Can update existing docs  
✅ **Delete works**: Can deprecate or remove docs  
✅ **Full CRUD**: Create, Read, Update, Delete all work  
✅ **All sprints work**: Complete system with no regressions  

---

## Sprint Completion Checklist

### After Each Sprint

- [ ] All new features work
- [ ] All previous sprint features still work  
- [ ] Tests pass
- [ ] Documentation updated
- [ ] Demo to stakeholder
- [ ] Git commit with sprint tag

### Final System (After Sprint 6)

You will have:
- ✅ **6 data sources**: Jira, GitHub, Confluence, GitLab, Slack, Google Docs
- ✅ **Smart tools**: LLM-powered distillation
- ✅ **Modular agent**: All 4 nodes
- ✅ **3 doc types**: Release notes, help docs, (+ more templates easy to add)
- ✅ **4 operations**: Create, audit, update, delete
- ✅ **Complete CLI**: All commands
- ✅ **Production ready**: Error handling, logging, caching

**And most importantly**: You built it incrementally, testing at each step, never in integration hell.

---

## Implementation Tips

### For Each Sprint

1. **Start fresh branch**: `git checkout -b sprint-N`
2. **Implement features**: Follow sprint plan
3. **Test thoroughly**: Run all tests, including previous sprints
4. **Demo**: Show working feature
5. **Merge**: `git merge sprint-N` (only if tests pass!)
6. **Tag**: `git tag sprint-N-complete`

### If Something Breaks

**In Sprint 1**: Fix architecture before proceeding
**In Sprint 2+**: Roll back to previous sprint, debug in isolation

### Success Metrics

- **Sprint 1 complete in 2 days** = Architecture is solid ✅
- **Sprint 1 takes > 3 days** = Architecture needs rethinking ⚠️
- **Any sprint breaks previous sprint** = Stop, debug, fix ⚠️

---

## Comparison: All-at-Once vs. Incremental

| Metric | All-at-Once | Incremental Sprints |
|--------|-------------|---------------------|
| **First working demo** | Week 8+ | Day 2 |
| **Integration complexity** | 36+ simultaneous | 2-4 per sprint |
| **Debug difficulty** | Nightmare | Manageable |
| **Risk** | High (all or nothing) | Low (working at each step) |
| **Stakeholder confidence** | Low (no demo) | High (see progress) |
| **Rollback cost** | Massive | One sprint |
| **Learning** | Delayed | Immediate |

---

## Next Steps

**Start with Sprint 1**:
1. Set up scaffolding (Phase 0)
2. Implement Jira + GitHub tools
3. Implement complete agent
4. Implement release notes operation
5. Test end-to-end
6. **Celebrate working system!** 🎉

Then Sprint 2, 3, 4, 5, 6... each building on solid foundation.

---

**Remember**: The goal is not to write code fast. The goal is to build a working, maintainable system. Incremental sprints ensure you always have a working system, never stuck in integration hell.

**Good luck!** 🚀

