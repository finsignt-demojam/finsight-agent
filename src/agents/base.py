"""
Base agent class with common functionality.
"""

from typing import Dict, Any
from langchain_openai import ChatOpenAI
from ..config import config


class BaseAgent:
    """Base class for all FinSight agents."""
    
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.llm = self._initialize_llm()
    
    def _initialize_llm(self) -> ChatOpenAI:
        """Initialize the LLM with Scaleway configuration."""
        return ChatOpenAI(
            model=config.scaleway.model,
            temperature=config.scaleway.temperature,
            max_tokens=config.scaleway.max_tokens,
            openai_api_key=config.scaleway.api_key,
            openai_api_base=config.scaleway.base_url,
        )
    
    def log(self, message: str, level: str = "INFO"):
        """Log a message."""
        print(f"[{level}] [{self.agent_name}] {message}")
    
    def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Process the agent's task. To be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement process method")

