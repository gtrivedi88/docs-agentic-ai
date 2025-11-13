"""
State definitions for the LangGraph agent.
"""
from typing import TypedDict, List, Dict, Any, Optional, Annotated
from langchain_core.messages import BaseMessage
from operator import add
from src.schemas.data_models import DocDraft, SourceReference


class AgentState(TypedDict):
    """Main agent state for documentation generation."""
    
    # User inputs
    user_goal: str
    doc_type: str
    release_version: Optional[str]
    topic: Optional[str]
    project_name: str
    
    # ReAct loop memory
    messages: Annotated[List[BaseMessage], add]
    
    # Knowledge gathering
    knowledge_bundle: Annotated[List[Dict[str, Any]], add]
    sources_explored: Annotated[List[str], add]
    
    # Document generation
    draft: Optional[DocDraft]
    revision_count: int
    
    # Quality control
    critique_notes: str
    quality_score: float
    approved: bool
    
    # Control flow
    next_action: str
    iterations: int
    max_iterations: int

