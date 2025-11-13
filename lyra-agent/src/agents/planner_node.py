"""
Planner node: Decides what information to gather next.
"""
from typing import Dict, Any
from langchain_mistralai import ChatMistralAI
from src.schemas.agent_state import AgentState
from src.tools.tool_registry import get_all_tools
from src.config.settings import settings
from src.agents.node_utils import load_prompts, summarize_knowledge, has_enough_knowledge
from src.utils.logger import logger


# Initialize LLM with tools (module-level, shared across calls)
_llm = ChatMistralAI(
    model=settings.mistral_model,
    api_key=settings.mistral_api_key,
    temperature=settings.temperature
)
_tools = get_all_tools()
_llm_with_tools = _llm.bind_tools(_tools)
_prompts = load_prompts()


def planner_node(state: AgentState) -> Dict[str, Any]:
    """
    Planning node: Decides what information to gather next.
    
    This node analyzes the current state and determines whether to:
    - Execute tools to gather more information
    - Move to synthesis (if enough knowledge gathered)
    - End (if max iterations reached)
    
    Args:
        state: Current agent state
        
    Returns:
        Updated state with next action
    """
    logger.info(f"Planning iteration {state['iterations']}")
    
    # Build planning prompt
    prompt = _prompts['planner_prompt'].format(
        goal=state['user_goal'],
        doc_type=state['doc_type'],
        explored=state['sources_explored'],
        knowledge_summary=summarize_knowledge(state['knowledge_bundle'])
    )
    
    # Get LLM decision
    response = _llm_with_tools.invoke([
        {"role": "system", "content": _prompts['controller_system_prompt'].format(
            project_name=state['project_name'],
            user_goal=state['user_goal']
        )},
        {"role": "user", "content": prompt}
    ])
    
    # Determine next action based on LLM response and state
    if response.tool_calls:
        next_action = "execute_tools"
        logger.debug(f"Planner decided to execute {len(response.tool_calls)} tool(s)")
    elif has_enough_knowledge(state):
        next_action = "synthesize"
        logger.info("Planner decided sufficient knowledge gathered, moving to synthesis")
    elif state['iterations'] >= state['max_iterations']:
        logger.warning("Max iterations reached, ending planning")
        next_action = "end"
    else:
        # Default: try to gather more info
        next_action = "execute_tools"
    
    return {
        "messages": [response],
        "next_action": next_action,
        "iterations": state['iterations'] + 1
    }

