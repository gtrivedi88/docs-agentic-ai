"""
GitHub integration tool using LangChain.
Provides tools for searching PRs, reading diffs, checking code.
"""
from typing import List, Optional
from github import Github, GithubException
from langchain.tools import tool
import json
import re
from datetime import datetime
from src.config.settings import settings
from src.schemas.data_models import GitHubPR
from src.tools.base_tool import BaseTool
from src.utils.logger import logger


class GitHubTool(BaseTool):
    """Tool for interacting with GitHub."""
    
    def _init_client(self):
        """Initialize GitHub client."""
        try:
            self.client = Github(settings.github_token)
            self.org = self.client.get_organization(settings.github_org)
            logger.info("GitHub client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize GitHub client: {e}")
            raise
    
    def search_prs(
        self,
        query: str,
        repo_name: Optional[str] = None,
        state: str = "all",
        max_results: int = 50
    ) -> List[GitHubPR]:
        """
        Search pull requests.
        
        Args:
            query: Search query (ticket ID, keywords, etc.)
            repo_name: Specific repo to search (optional)
            state: PR state (open, closed, all)
            max_results: Maximum results
            
        Returns:
            List of GitHubPR models
        """
        cache_key = self._cache_key("search_prs", query=query, repo=repo_name, state=state)
        cached = self._get_cached(cache_key)
        if cached:
            return [GitHubPR(**pr) for pr in cached]
        
        try:
            prs = []
            repos_to_search = [repo_name] if repo_name else settings.github_repo_list
            
            for repo_full_name in repos_to_search:
                logger.debug(f"Searching PRs in {repo_full_name} for: {query}")
                repo = self.client.get_repo(repo_full_name)
                
                # Search in title and body
                pulls = repo.get_pulls(state=state)
                for pr in pulls[:max_results]:
                    if query.lower() in pr.title.lower() or (pr.body and query.lower() in pr.body.lower()):
                        pr_model = self._pr_to_model(pr)
                        prs.append(pr_model)
            
            self._set_cached(cache_key, [pr.model_dump() for pr in prs])
            logger.info(f"Found {len(prs)} PRs matching: {query}")
            return prs
            
        except Exception as e:
            self._handle_error(e, "search_prs")
    
    def get_pr_details(self, repo_name: str, pr_number: int) -> GitHubPR:
        """
        Get detailed information about a specific PR.
        
        Args:
            repo_name: Repository name (e.g., "your-org/developerhub")
            pr_number: PR number
            
        Returns:
            GitHubPR model
        """
        cache_key = self._cache_key("get_pr", repo=repo_name, pr=pr_number)
        cached = self._get_cached(cache_key)
        if cached:
            return GitHubPR(**cached)
        
        try:
            logger.debug(f"Fetching PR details: {repo_name}#{pr_number}")
            repo = self.client.get_repo(repo_name)
            pr = repo.get_pull(pr_number)
            pr_model = self._pr_to_model(pr, include_diff=True)
            
            self._set_cached(cache_key, pr_model.model_dump())
            return pr_model
            
        except Exception as e:
            self._handle_error(e, f"get_pr_details({repo_name}#{pr_number})")
    
    def find_prs_for_ticket(self, ticket_id: str) -> List[GitHubPR]:
        """
        Find all PRs that reference a specific Jira ticket.
        
        Args:
            ticket_id: Jira ticket ID (e.g., DEV-123)
            
        Returns:
            List of GitHubPR models
        """
        return self.search_prs(query=ticket_id)
    
    def get_file_content(self, repo_name: str, file_path: str, branch: str = "main") -> str:
        """
        Get content of a specific file from repository.
        
        Args:
            repo_name: Repository name
            file_path: Path to file
            branch: Branch name
            
        Returns:
            File content as string
        """
        try:
            repo = self.client.get_repo(repo_name)
            content = repo.get_contents(file_path, ref=branch)
            return content.decoded_content.decode('utf-8')
        except Exception as e:
            logger.warning(f"Could not fetch {file_path}: {e}")
            return ""
    
    def check_file_exists(self, repo_name: str, file_path: str, branch: str = "main") -> bool:
        """
        Check if a file exists in the repository.
        
        Args:
            repo_name: Repository name
            file_path: Path to file
            branch: Branch name
            
        Returns:
            True if file exists
        """
        try:
            repo = self.client.get_repo(repo_name)
            repo.get_contents(file_path, ref=branch)
            return True
        except GithubException:
            return False
    
    def _pr_to_model(self, pr, include_diff: bool = False) -> GitHubPR:
        """Convert GitHub PR to GitHubPR model."""
        # Extract linked Jira tickets from title and body
        linked_issues = []
        text_to_search = f"{pr.title} {pr.body or ''}"
        # Match JIRA ticket patterns like DEV-123
        matches = re.findall(r'[A-Z]+-\d+', text_to_search)
        linked_issues = list(set(matches))
        
        # Get diff summary if requested
        diff_summary = None
        if include_diff:
            files = pr.get_files()
            changed_files = [f.filename for f in files[:10]]  # First 10 files
            diff_summary = f"Changed files: {', '.join(changed_files)}"
            if pr.changed_files > 10:
                diff_summary += f" (and {pr.changed_files - 10} more)"
        
        return GitHubPR(
            id=pr.id,
            number=pr.number,
            title=pr.title,
            body=pr.body,
            state=pr.state,
            author=pr.user.login,
            created_at=pr.created_at,
            updated_at=pr.updated_at,
            merged_at=pr.merged_at,
            merged_by=pr.merged_by.login if pr.merged_by else None,
            base_branch=pr.base.ref,
            head_branch=pr.head.ref,
            files_changed=pr.changed_files,
            additions=pr.additions,
            deletions=pr.deletions,
            diff_summary=diff_summary,
            linked_issues=linked_issues,
            labels=[label.name for label in pr.labels],
            url=pr.html_url
        )


# LangChain tool wrappers
github_tool = GitHubTool()


@tool
def search_github_prs(query: str, repo_name: Optional[str] = None, max_results: int = 20) -> str:
    """
    Search GitHub pull requests by query string.
    
    Args:
        query: Search query (ticket ID, keywords, etc.)
        repo_name: Optional specific repository to search
        max_results: Maximum number of results
        
    Returns:
        JSON string with list of PRs
    """
    prs = github_tool.search_prs(query, repo_name, max_results=max_results)
    return json.dumps([pr.model_dump(mode='json') for pr in prs], indent=2, default=str)


@tool
def get_github_pr(repo_name: str, pr_number: int) -> str:
    """
    Get detailed information about a specific GitHub PR including diff summary.
    
    Args:
        repo_name: Repository name (e.g., "your-org/developerhub")
        pr_number: PR number
        
    Returns:
        JSON string with PR details
    """
    pr = github_tool.get_pr_details(repo_name, pr_number)
    return json.dumps(pr.model_dump(mode='json'), indent=2, default=str)


@tool
def find_github_prs_for_ticket(ticket_id: str) -> str:
    """
    Find all GitHub PRs that reference a specific Jira ticket.
    
    Args:
        ticket_id: Jira ticket ID (e.g., DEV-123)
        
    Returns:
        JSON string with list of PRs
    """
    prs = github_tool.find_prs_for_ticket(ticket_id)
    return json.dumps([pr.model_dump(mode='json') for pr in prs], indent=2, default=str)


@tool
def check_github_file_exists(repo_name: str, file_path: str, branch: str = "main") -> str:
    """
    Check if a file exists in a GitHub repository.
    Useful for validating if documented features/APIs still exist.
    
    Args:
        repo_name: Repository name
        file_path: Path to file
        branch: Branch name (default: main)
        
    Returns:
        JSON string with existence check result
    """
    exists = github_tool.check_file_exists(repo_name, file_path, branch)
    return json.dumps({"exists": exists, "repo": repo_name, "path": file_path, "branch": branch})

