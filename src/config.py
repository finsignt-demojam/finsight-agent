"""
Configuration module for FinSight Agent.
Handles environment variables and API configurations.
"""

import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


@dataclass
class ScalewayConfig:
    """Scaleway GenAI API configuration."""
    project_id: str
    api_key: str
    model: str = "qwen3-235b-a22b-instruct-2507"
    temperature: float = 0.0
    max_tokens: int = 2048
    
    @property
    def base_url(self) -> str:
        return f"https://api.scaleway.ai/{self.project_id}/v1"


@dataclass
class APIConfig:
    """External API configurations."""
    tavily_search_api_key: str
    google_api_key: Optional[str] = None


@dataclass
class SECConfig:
    """SEC EDGAR configuration."""
    company_name: str = "FinSightAI"
    email: str = "research@finsight.ai"


@dataclass
class PathConfig:
    """File path configurations."""
    output_dir: str = "./data/output"
    input_dir: str = "./data/input"


class Config:
    """Main configuration class for FinSight Agent."""
    
    def __init__(self):
        # Scaleway Configuration
        self.scaleway = ScalewayConfig(
            project_id=os.getenv("SCW_DEFAULT_PROJECT_ID", ""),
            api_key=os.getenv("SCW_SECRET_KEY", ""),
        )
        
        # API Configuration
        self.api = APIConfig(
            tavily_search_api_key=os.getenv("TAVILY_API_KEY", ""),
            google_api_key=os.getenv("GOOGLE_API_KEY", ""),
        )
        
        # SEC Configuration
        self.sec = SECConfig()
        
        # Path Configuration
        self.paths = PathConfig()
    
    def validate(self) -> bool:
        """Validate that required configurations are present."""
        required_checks = [
            (self.scaleway.project_id, "SCW_DEFAULT_PROJECT_ID"),
            (self.scaleway.api_key, "SCW_SECRET_KEY"),
            (self.api.tavily_search_api_key, "TAVILY_API_KEY"),
        ]
        
        missing = [name for value, name in required_checks if not value]
        
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")
        
        return True


# Global configuration instance
config = Config()

