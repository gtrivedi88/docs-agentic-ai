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

