"""
Executor node: Executes tool calls requested by planner.
"""
from typing import Dict, Any, List
from src.schemas.agent_state import AgentState
from src.tools.tool_registry import get_all_tools
from src.utils.logger import logger


# Get tools once at module level
_tools = get_all_tools()


def executor_node(state: AgentState) -> Dict[str, Any]:
    """
    Executor node: Executes tool calls.
    
    This node takes tool calls from the planner's last message and executes them,
    gathering knowledge from various data sources.
    
    Args:
        state: Current agent state
        
    Returns:
        Updated state with tool results added to knowledge bundle
    """
    last_message = state['messages'][-1]
    
    # Check if there are tool calls to execute
    if not hasattr(last_message, 'tool_calls') or not last_message.tool_calls:
        logger.debug("No tool calls to execute")
        return {}
    
    logger.info(f"Executing {len(last_message.tool_calls)} tool(s)")
    
    new_knowledge = []
    new_sources = []
    
    # Execute each tool call
    for tool_call in last_message.tool_calls:
        tool_name = tool_call['name']
        tool_args = tool_call['args']
        
        logger.debug(f"Calling tool: {tool_name} with args: {tool_args}")
        
        # Find the tool
        tool = next((t for t in _tools if t.name == tool_name), None)
        
        if not tool:
            logger.error(f"Tool not found: {tool_name}")
            continue
        
        # Execute tool
        try:
            result = tool.invoke(tool_args)
            
            # Add to knowledge bundle
            new_knowledge.append({
                "source": tool_name,
                "data": result,
                "query": str(tool_args)
            })
            
            # Track source type (e.g., 'jira' from 'search_jira_tickets')
            source_type = tool_name.split('_')[0]
            if source_type not in state['sources_explored']:
                new_sources.append(source_type)
            
            logger.info(f"Successfully executed {tool_name}")
            
        except Exception as e:
            logger.error(f"Tool execution failed for {tool_name}: {e}")
            # Add error to knowledge bundle so agent is aware
            new_knowledge.append({
                "source": tool_name,
                "data": f"ERROR: {str(e)}",
                "query": str(tool_args)
            })
    
    return {
        "knowledge_bundle": new_knowledge,
        "sources_explored": new_sources
    }

