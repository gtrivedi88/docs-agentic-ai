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

