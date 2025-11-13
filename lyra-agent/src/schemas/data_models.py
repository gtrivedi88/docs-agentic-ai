"""
Core data models for Lyra.
All data from external sources is normalized into these models.
"""
from datetime import datetime
from typing import Optional, List, Dict, Any, Literal
from pydantic import BaseModel, Field, HttpUrl


class SourceReference(BaseModel):
    """Reference to an external source."""
    source_type: Literal["jira", "github", "gitlab", "confluence", "slack", "gdocs"]
    source_id: str = Field(..., description="Ticket ID, PR number, page ID, etc.")
    url: HttpUrl
    title: str
    excerpt: Optional[str] = Field(None, description="Relevant excerpt from source")
    timestamp: datetime
    metadata: Dict[str, Any] = Field(default_factory=dict)


class JiraTicket(BaseModel):
    """Jira ticket data model."""
    id: str = Field(..., description="Ticket ID (e.g., DEV-123)")
    key: str = Field(..., description="Ticket key")
    summary: str
    description: Optional[str] = None
    status: str
    priority: str
    issue_type: str
    assignee: Optional[str] = None
    reporter: str
    created: datetime
    updated: datetime
    resolved: Optional[datetime] = None
    fix_versions: List[str] = Field(default_factory=list)
    components: List[str] = Field(default_factory=list)
    labels: List[str] = Field(default_factory=list)
    comments: List["JiraComment"] = Field(default_factory=list)
    linked_issues: List[str] = Field(default_factory=list, description="Related ticket IDs")
    url: HttpUrl
    
    
class JiraComment(BaseModel):
    """Jira comment data model."""
    id: str
    author: str
    body: str
    created: datetime
    updated: Optional[datetime] = None


class GitHubPR(BaseModel):
    """GitHub pull request data model."""
    id: int
    number: int
    title: str
    body: Optional[str] = None
    state: str
    author: str
    created_at: datetime
    updated_at: datetime
    merged_at: Optional[datetime] = None
    merged_by: Optional[str] = None
    base_branch: str
    head_branch: str
    files_changed: int
    additions: int
    deletions: int
    diff_summary: Optional[str] = Field(None, description="Summarized diff")
    linked_issues: List[str] = Field(default_factory=list, description="Referenced issues")
    labels: List[str] = Field(default_factory=list)
    url: HttpUrl


class ConfluencePage(BaseModel):
    """Confluence page data model."""
    id: str
    title: str
    space_key: str
    content: str = Field(..., description="Page content (HTML or markdown)")
    version: int
    author: str
    created: datetime
    updated: datetime
    url: HttpUrl
    labels: List[str] = Field(default_factory=list)
    parent_id: Optional[str] = None


class SlackMessage(BaseModel):
    """Slack message data model."""
    timestamp: str = Field(..., description="Slack message timestamp")
    channel: str
    user: str
    text: str
    thread_ts: Optional[str] = Field(None, description="Thread timestamp if part of thread")
    reactions: List[str] = Field(default_factory=list)
    url: str


class GoogleDoc(BaseModel):
    """Google Doc data model."""
    id: str
    title: str
    content: str
    created: datetime
    updated: datetime
    owner: str
    url: HttpUrl


class Citation(BaseModel):
    """Citation for a claim in generated documentation."""
    claim: str = Field(..., description="The claim being made")
    sources: List[SourceReference] = Field(..., description="Supporting sources")
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence in this claim")
    verified: bool = Field(default=False, description="Whether claim was verified")


class DocDraft(BaseModel):
    """Generated documentation draft."""
    doc_type: Literal["release_notes", "help_doc", "api_reference", "tutorial", "troubleshooting", "feature_doc"]
    title: str
    content: str = Field(..., description="Full markdown content")
    citations: List[Citation] = Field(default_factory=list)
    sources_consulted: List[SourceReference] = Field(default_factory=list)
    confidence_score: float = Field(ge=0.0, le=1.0, description="Overall confidence")
    needs_review_sections: List[str] = Field(default_factory=list, description="Sections flagged for review")
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.now)


class AuditResult(BaseModel):
    """Result from documentation audit."""
    doc_path: str
    status: Literal["current", "outdated", "deprecated", "orphaned"]
    reason: str
    recommendation: Literal["keep", "update", "delete"]
    related_sources: List[SourceReference] = Field(default_factory=list)
    confidence: float = Field(ge=0.0, le=1.0)

