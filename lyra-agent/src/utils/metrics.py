"""
Metrics and tracking utilities.
"""
import time
from typing import Dict, Any
from dataclasses import dataclass, field
from src.utils.logger import logger


@dataclass
class AgentMetrics:
    """Track agent execution metrics."""
    
    start_time: float = field(default_factory=time.time)
    end_time: float = 0.0
    tool_calls: int = 0
    tokens_used: int = 0
    estimated_cost: float = 0.0
    iterations: int = 0
    sources_consulted: list = field(default_factory=list)
    
    def finish(self):
        """Mark execution as finished."""
        self.end_time = time.time()
    
    @property
    def duration(self) -> float:
        """Get execution duration in seconds."""
        end = self.end_time or time.time()
        return end - self.start_time
    
    def log_summary(self):
        """Log metrics summary."""
        logger.info(f"""
        === Agent Execution Summary ===
        Duration: {self.duration:.2f}s
        Iterations: {self.iterations}
        Tool Calls: {self.tool_calls}
        Sources: {', '.join(self.sources_consulted)}
        Tokens: {self.tokens_used}
        Est. Cost: ${self.estimated_cost:.4f}
        """)

