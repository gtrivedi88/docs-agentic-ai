"""
Shared utilities for agent nodes.
"""
from typing import Dict, Any, List
import yaml
from src.utils.logger import logger


def load_prompts() -> Dict[str, str]:
    """Load all prompts from YAML file."""
    with open("src/config/prompts.yaml", "r") as f:
        return yaml.safe_load(f)


def summarize_knowledge(knowledge_bundle: List[Dict]) -> str:
    """
    Summarize gathered knowledge for display.
    
    Args:
        knowledge_bundle: List of knowledge items
        
    Returns:
        Human-readable summary
    """
    if not knowledge_bundle:
        return "No knowledge gathered yet."
    
    sources = set(k['source'] for k in knowledge_bundle)
    return f"Gathered {len(knowledge_bundle)} pieces of information from {len(sources)} sources."


def format_knowledge_for_synthesis(knowledge_bundle: List[Dict]) -> str:
    """
    Format knowledge bundle for synthesis prompt.
    
    Args:
        knowledge_bundle: List of knowledge items
        
    Returns:
        Formatted string for LLM prompt
    """
    formatted = []
    for item in knowledge_bundle:
        # Truncate data to avoid huge prompts
        data_preview = item['data'][:500] if len(item['data']) > 500 else item['data']
        formatted.append(
            f"Source: {item['source']}\n"
            f"Query: {item['query']}\n"
            f"Data: {data_preview}{'...' if len(item['data']) > 500 else ''}\n"
        )
    return "\n---\n".join(formatted)


def extract_title_from_content(content: str) -> str:
    """
    Extract title from markdown content.
    
    Args:
        content: Markdown content
        
    Returns:
        Extracted title or default
    """
    lines = content.split('\n')
    for line in lines:
        if line.startswith('# '):
            return line.replace('# ', '').strip()
    return "Untitled Document"


def has_enough_knowledge(state: Dict[str, Any]) -> bool:
    """
    Determine if agent has gathered enough knowledge.
    
    Args:
        state: Current agent state
        
    Returns:
        True if sufficient knowledge gathered
    """
    # Heuristic: at least 2 sources and 3 knowledge items
    return (
        len(state.get('sources_explored', [])) >= 2 and
        len(state.get('knowledge_bundle', [])) >= 3
    )

