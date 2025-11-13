"""
Jira integration tool using LangChain.
Provides tools for searching tickets, reading comments, following links.
"""
from typing import List, Optional
from jira import JIRA
from langchain.tools import tool
from datetime import datetime
import json
from src.config.settings import settings
from src.schemas.data_models import JiraTicket, JiraComment
from src.tools.base_tool import BaseTool
from src.utils.logger import logger


class JiraTool(BaseTool):
    """Tool for interacting with Jira."""
    
    def _init_client(self):
        """Initialize Jira client."""
        try:
            self.client = JIRA(
                server=settings.jira_server,
                basic_auth=(settings.jira_user, settings.jira_api_token)
            )
            logger.info("Jira client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Jira client: {e}")
            raise
    
    def search_tickets(
        self, 
        jql: str, 
        max_results: int = 50,
        expand_comments: bool = True
    ) -> List[JiraTicket]:
        """
        Search Jira tickets using JQL.
        
        Args:
            jql: JQL query string
            max_results: Maximum number of results
            expand_comments: Whether to fetch comments
            
        Returns:
            List of JiraTicket models
        """
        cache_key = self._cache_key("search_tickets", jql=jql, max_results=max_results)
        cached = self._get_cached(cache_key)
        if cached:
            return [JiraTicket(**t) for t in cached]
        
        try:
            logger.info(f"Searching Jira with JQL: {jql}")
            expand_fields = "changelog" if expand_comments else None
            issues = self.client.search_issues(
                jql, 
                maxResults=max_results,
                expand=expand_fields
            )
            
            tickets = []
            for issue in issues:
                ticket = self._issue_to_model(issue, expand_comments)
                tickets.append(ticket)
            
            # Cache results
            self._set_cached(cache_key, [t.model_dump() for t in tickets])
            
            logger.info(f"Found {len(tickets)} tickets")
            return tickets
            
        except Exception as e:
            self._handle_error(e, "search_tickets")
    
    def get_ticket_details(self, ticket_id: str, include_comments: bool = True) -> JiraTicket:
        """
        Get detailed information about a specific ticket.
        
        Args:
            ticket_id: Jira ticket ID (e.g., DEV-123)
            include_comments: Whether to fetch comments
            
        Returns:
            JiraTicket model
        """
        cache_key = self._cache_key("get_ticket", ticket_id=ticket_id)
        cached = self._get_cached(cache_key)
        if cached:
            return JiraTicket(**cached)
        
        try:
            logger.debug(f"Fetching ticket details: {ticket_id}")
            issue = self.client.issue(ticket_id, expand="changelog")
            ticket = self._issue_to_model(issue, include_comments)
            
            self._set_cached(cache_key, ticket.model_dump())
            return ticket
            
        except Exception as e:
            self._handle_error(e, f"get_ticket_details({ticket_id})")
    
    def get_tickets_for_release(self, release_version: str) -> List[JiraTicket]:
        """
        Get all tickets for a specific release version.
        
        Args:
            release_version: Release version (e.g., "v2.1")
            
        Returns:
            List of JiraTicket models
        """
        jql = f'project = {settings.project_key} AND fixVersion = "{release_version}" ORDER BY created DESC'
        return self.search_tickets(jql)
    
    def follow_linked_issues(self, ticket_id: str) -> List[JiraTicket]:
        """
        Follow links from a ticket and get all related tickets.
        
        Args:
            ticket_id: Source ticket ID
            
        Returns:
            List of linked tickets
        """
        try:
            issue = self.client.issue(ticket_id)
            linked_tickets = []
            
            # Get linked issues
            for link in issue.fields.issuelinks:
                if hasattr(link, 'outwardIssue'):
                    linked_id = link.outwardIssue.key
                elif hasattr(link, 'inwardIssue'):
                    linked_id = link.inwardIssue.key
                else:
                    continue
                
                linked_ticket = self.get_ticket_details(linked_id)
                linked_tickets.append(linked_ticket)
            
            logger.debug(f"Found {len(linked_tickets)} linked tickets for {ticket_id}")
            return linked_tickets
            
        except Exception as e:
            self._handle_error(e, f"follow_linked_issues({ticket_id})")
    
    def _issue_to_model(self, issue, include_comments: bool = True) -> JiraTicket:
        """Convert Jira issue to JiraTicket model."""
        fields = issue.fields
        
        # Parse comments
        comments = []
        if include_comments and hasattr(fields, 'comment') and fields.comment:
            for comment in fields.comment.comments:
                comments.append(JiraComment(
                    id=comment.id,
                    author=comment.author.displayName,
                    body=comment.body,
                    created=datetime.fromisoformat(comment.created.replace('Z', '+00:00')),
                    updated=datetime.fromisoformat(comment.updated.replace('Z', '+00:00')) if comment.updated else None
                ))
        
        # Parse linked issues
        linked_issues = []
        if hasattr(fields, 'issuelinks'):
            for link in fields.issuelinks:
                if hasattr(link, 'outwardIssue'):
                    linked_issues.append(link.outwardIssue.key)
                elif hasattr(link, 'inwardIssue'):
                    linked_issues.append(link.inwardIssue.key)
        
        return JiraTicket(
            id=issue.id,
            key=issue.key,
            summary=fields.summary,
            description=fields.description or "",
            status=fields.status.name,
            priority=fields.priority.name if fields.priority else "Unknown",
            issue_type=fields.issuetype.name,
            assignee=fields.assignee.displayName if fields.assignee else None,
            reporter=fields.reporter.displayName if fields.reporter else "Unknown",
            created=datetime.fromisoformat(fields.created.replace('Z', '+00:00')),
            updated=datetime.fromisoformat(fields.updated.replace('Z', '+00:00')),
            resolved=datetime.fromisoformat(fields.resolutiondate.replace('Z', '+00:00')) if fields.resolutiondate else None,
            fix_versions=[v.name for v in fields.fixVersions] if fields.fixVersions else [],
            components=[c.name for c in fields.components] if fields.components else [],
            labels=fields.labels or [],
            comments=comments,
            linked_issues=linked_issues,
            url=f"{settings.jira_server}/browse/{issue.key}"
        )


# LangChain tool wrappers
jira_tool = JiraTool()


@tool
def search_jira_tickets(jql: str, max_results: int = 50) -> str:
    """
    Search Jira tickets using JQL query.
    
    Args:
        jql: JQL query string
        max_results: Maximum number of results (default: 50)
        
    Returns:
        JSON string with list of tickets
    """
    tickets = jira_tool.search_tickets(jql, max_results)
    return json.dumps([t.model_dump(mode='json') for t in tickets], indent=2, default=str)


@tool
def get_jira_ticket(ticket_id: str) -> str:
    """
    Get detailed information about a specific Jira ticket including comments.
    
    Args:
        ticket_id: Jira ticket ID (e.g., DEV-123)
        
    Returns:
        JSON string with ticket details
    """
    ticket = jira_tool.get_ticket_details(ticket_id)
    return json.dumps(ticket.model_dump(mode='json'), indent=2, default=str)


@tool
def get_jira_release_tickets(release_version: str) -> str:
    """
    Get all Jira tickets for a specific release version.
    
    Args:
        release_version: Release version (e.g., "v2.1")
        
    Returns:
        JSON string with list of tickets
    """
    tickets = jira_tool.get_tickets_for_release(release_version)
    return json.dumps([t.model_dump(mode='json') for t in tickets], indent=2, default=str)


@tool
def get_linked_jira_tickets(ticket_id: str) -> str:
    """
    Get all tickets linked to a specific Jira ticket.
    
    Args:
        ticket_id: Source ticket ID
        
    Returns:
        JSON string with list of linked tickets
    """
    tickets = jira_tool.follow_linked_issues(ticket_id)
    return json.dumps([t.model_dump(mode='json') for t in tickets], indent=2, default=str)

