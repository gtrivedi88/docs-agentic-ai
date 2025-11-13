"""
Base tool class with common functionality.
"""
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
import hashlib
import json
import time
from pathlib import Path
from src.config.settings import settings
from src.utils.logger import logger


class BaseTool(ABC):
    """Base class for all data source tools."""
    
    def __init__(self, cache_enabled: bool = None):
        """
        Initialize base tool.
        
        Args:
            cache_enabled: Override default cache setting
        """
        self.cache_enabled = cache_enabled if cache_enabled is not None else settings.enable_cache
        self.cache_dir = Path("./data/cache") / self.__class__.__name__.lower()
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self._init_client()
    
    @abstractmethod
    def _init_client(self):
        """Initialize the API client. Implemented by subclasses."""
        pass
    
    def _cache_key(self, method: str, **kwargs) -> str:
        """Generate cache key from method and parameters."""
        key_data = f"{method}:{json.dumps(kwargs, sort_keys=True)}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def _get_cached(self, key: str) -> Optional[Any]:
        """Retrieve cached response if exists and not expired."""
        if not self.cache_enabled:
            return None
        
        cache_file = self.cache_dir / f"{key}.json"
        if not cache_file.exists():
            return None
        
        try:
            with open(cache_file, 'r') as f:
                cached = json.load(f)
            
            # Check if expired
            if time.time() - cached['timestamp'] > settings.cache_ttl:
                cache_file.unlink()
                return None
            
            logger.debug(f"Cache hit for {key}")
            return cached['data']
        except Exception as e:
            logger.warning(f"Cache read error: {e}")
            return None
    
    def _set_cached(self, key: str, data: Any):
        """Store response in cache."""
        if not self.cache_enabled:
            return
        
        cache_file = self.cache_dir / f"{key}.json"
        try:
            with open(cache_file, 'w') as f:
                json.dump({
                    'timestamp': time.time(),
                    'data': data
                }, f)
            logger.debug(f"Cached result for {key}")
        except Exception as e:
            logger.warning(f"Cache write error: {e}")
    
    def _handle_error(self, error: Exception, context: str) -> None:
        """Standardized error handling."""
        logger.error(f"Error in {self.__class__.__name__}.{context}: {error}")
        raise

