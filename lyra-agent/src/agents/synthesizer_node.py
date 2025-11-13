"""
Synthesizer node: Generates documentation from gathered knowledge.
"""
from typing import Dict, Any
from langchain_mistralai import ChatMistralAI
from src.schemas.agent_state import AgentState
from src.schemas.data_models import DocDraft
from src.config.settings import settings
from src.agents.node_utils import load_prompts, format_knowledge_for_synthesis, extract_title_from_content
from src.utils.logger import logger


# Initialize LLM at module level
_llm = ChatMistralAI(
    model=settings.mistral_model,
    api_key=settings.mistral_api_key,
    temperature=0.3  # Slightly higher for creative writing
)
_prompts = load_prompts()


def synthesizer_node(state: AgentState) -> Dict[str, Any]:
    """
    Synthesizer node: Generates documentation from gathered knowledge.
    
    This node takes all gathered knowledge and synthesizes it into
    a complete documentation draft.
    
    Args:
        state: Current agent state
        
    Returns:
        Updated state with draft document
    """
    logger.info("Synthesizing documentation")
    
    # Get style examples from existing docs
    try:
        from src.services.knowledge_service import KnowledgeService
        knowledge_service = KnowledgeService()
        style_examples = knowledge_service.get_style_examples(state['doc_type'], n_examples=2)
    except Exception as e:
        logger.warning(f"Could not load style examples: {e}")
        style_examples = []
    
    # Build synthesis prompt
    prompt = _prompts['synthesizer_prompt'].format(
        doc_type=state['doc_type'],
        audience="technical users",  # TODO: Make configurable
        knowledge_bundle=format_knowledge_for_synthesis(state['knowledge_bundle']),
        style_examples="\n\n---\n\n".join(style_examples) if style_examples else "No style examples available"
    )
    
    # Generate documentation
    logger.debug("Calling LLM for documentation generation")
    response = _llm.invoke([
        {"role": "system", "content": "You are a technical writer creating documentation."},
        {"role": "user", "content": prompt}
    ])
    
    # Create draft object
    draft = DocDraft(
        doc_type=state['doc_type'],
        title=extract_title_from_content(response.content),
        content=response.content,
        citations=[],  # TODO: Extract citations from content
        sources_consulted=[],
        confidence_score=0.8,  # TODO: Calculate based on knowledge quality
        needs_review_sections=[],
        metadata={
            "sources_used": state['sources_explored'],
            "knowledge_items": len(state['knowledge_bundle'])
        }
    )
    
    logger.info(f"Generated draft: {draft.title}")
    
    return {
        "draft": draft,
        "revision_count": state.get('revision_count', 0) + 1
    }

