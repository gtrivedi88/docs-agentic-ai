"""
Critic node: Reviews documentation quality and provides feedback.
"""
from typing import Dict, Any
from langchain_mistralai import ChatMistralAI
from src.schemas.agent_state import AgentState
from src.config.settings import settings
from src.agents.node_utils import load_prompts
from src.utils.logger import logger


# Initialize LLM at module level
_llm = ChatMistralAI(
    model=settings.mistral_model,
    api_key=settings.mistral_api_key,
    temperature=0.1  # Low temperature for consistent critique
)
_prompts = load_prompts()


def critic_node(state: AgentState) -> Dict[str, Any]:
    """
    Critic node: Reviews documentation quality.
    
    This node evaluates the generated documentation for:
    - Accuracy and factual correctness
    - Completeness
    - Clarity and readability
    - Proper structure and formatting
    - Style consistency
    
    Args:
        state: Current agent state
        
    Returns:
        Updated state with critique and approval decision
    """
    logger.info("Critiquing documentation")
    
    # Check if there's a draft to review
    if not state.get('draft'):
        logger.warning("No draft available to critique")
        return {
            "approved": False,
            "critique_notes": "No draft to review",
            "quality_score": 0.0
        }
    
    draft = state['draft']
    
    # Build critique prompt
    prompt = _prompts['critic_prompt'].format(
        draft=draft.content
    )
    
    # Get critique from LLM
    logger.debug("Calling LLM for quality review")
    response = _llm.invoke([
        {"role": "system", "content": "You are a documentation quality reviewer."},
        {"role": "user", "content": prompt}
    ])
    
    critique_text = response.content
    
    # Parse critique to determine approval
    # In production, use structured output (JSON mode)
    critique_lower = critique_text.lower()
    approved = any(keyword in critique_lower for keyword in [
        "approved",
        "good quality",
        "ready to publish",
        "meets standards"
    ])
    
    # Calculate quality score (simplified heuristic)
    if approved:
        quality_score = 0.9
    elif "minor issues" in critique_lower:
        quality_score = 0.7
    elif "major issues" in critique_lower:
        quality_score = 0.5
    else:
        quality_score = 0.6
    
    logger.info(f"Critique complete: approved={approved}, score={quality_score}")
    
    return {
        "critique_notes": critique_text,
        "quality_score": quality_score,
        "approved": approved
    }

