"""
Agent implementations for FinSight Agent.
"""

from .coordinator import CoordinatorAgent
from .sentiment import SentimentAnalysisAgent
from .events import EventDetectionAgent
from .volatility import VolatilityPredictionAgent

__all__ = [
    "CoordinatorAgent",
    "SentimentAnalysisAgent",
    "EventDetectionAgent",
    "VolatilityPredictionAgent",
]

