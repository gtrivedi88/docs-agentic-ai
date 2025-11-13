"""
Controller: Assembles the agent graph from modular nodes.

This file's only job is to wire together the agent nodes into a LangGraph workflow.
All node logic lives in separate files for modularity and testability.
"""
from langgraph.graph import StateGraph, END
from src.schemas.agent_state import AgentState
from src.agents.planner_node import planner_node
from src.agents.executor_node import executor_node
from src.agents.synthesizer_node import synthesizer_node
from src.agents.critic_node import critic_node
from src.utils.logger import logger


def route_after_planning(state: AgentState) -> str:
    """
    Route after planning node.
    
    Args:
        state: Current agent state
        
    Returns:
        Next node name
    """
    return state.get('next_action', 'execute_tools')


def route_after_synthesis(state: AgentState) -> str:
    """
    Route after synthesis node.
    
    Args:
        state: Current agent state
        
    Returns:
        Next node name
    """
    if state.get('draft'):
        return "critique"
    return "end"


def route_after_critique(state: AgentState) -> str:
    """
    Route after critique node.
    
    Args:
        state: Current agent state
        
    Returns:
        Next node name
    """
    if state.get('approved', False):
        logger.info("Draft approved by critic")
        return "approved"
    
    if state.get('revision_count', 0) >= 3:
        logger.warning("Max revisions reached, accepting draft")
        return "max_revisions"
    
    logger.info("Draft needs revision, returning to synthesizer")
    return "revise"


def create_lyra_agent():
    """
    Create and return the Lyra agent graph.
    
    This function assembles all the modular agent nodes into a complete
    LangGraph workflow with proper edges and routing.
    
    Returns:
        Compiled LangGraph agent
    """
    logger.info("Creating Lyra agent graph")
    
    # Create workflow
    workflow = StateGraph(AgentState)
    
    # Add nodes (all imported from separate files)
    workflow.add_node("planner", planner_node)
    workflow.add_node("executor", executor_node)
    workflow.add_node("synthesizer", synthesizer_node)
    workflow.add_node("critic", critic_node)
    
    # Set entry point
    workflow.set_entry_point("planner")
    
    # Add conditional edges with routing functions
    workflow.add_conditional_edges(
        "planner",
        route_after_planning,
        {
            "execute_tools": "executor",
            "synthesize": "synthesizer",
            "end": END
        }
    )
    
    # Executor loops back to planner for next decision
    workflow.add_edge("executor", "planner")
    
    workflow.add_conditional_edges(
        "synthesizer",
        route_after_synthesis,
        {
            "critique": "critic",
            "end": END
        }
    )
    
    workflow.add_conditional_edges(
        "critic",
        route_after_critique,
        {
            "revise": "synthesizer",
            "approved": END,
            "max_revisions": END
        }
    )
    
    # Compile and return
    compiled_graph = workflow.compile()
    logger.info("Lyra agent graph created successfully")
    
    return compiled_graph

