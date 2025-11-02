"""
Data models for FinSight Agent.
Defines all Pydantic models for structured data.
"""

from typing import List, Dict, Any, Optional, Literal
from pydantic import BaseModel, Field
from datetime import datetime


# --- Analysis Question Models ---

class AnalysisQuestion(BaseModel):
    """A question to be answered from the earnings call transcript."""
    category: str = Field(description="Category of the question")
    focus_item: str = Field(description="Specific focus area within the category")
    question: str = Field(description="The actual question to be answered")
    priority: Literal["high", "medium", "low"] = Field(default="medium")


# --- Agent Output Models ---

class SentimentAnalysisResult(BaseModel):
    """Result from sentiment analysis agent."""
    overall_sentiment: Literal["very_positive", "positive", "neutral", "negative", "very_negative"]
    sentiment_score: float = Field(description="Numerical sentiment score from -1.0 to 1.0")
    market_sentiment: str = Field(description="Summary of broader market sentiment")
    key_sentiment_drivers: List[str] = Field(description="Key topics driving the sentiment")
    news_headlines: List[str] = Field(default_factory=list)
    confidence: float = Field(description="Confidence in sentiment assessment (0-1)")
    tool_validations: List[str] = Field(default_factory=list, description="Tools used for validation")


class SignificantEvent(BaseModel):
    """A significant event detected and validated."""
    event_type: str = Field(description="Type of event")
    description: str = Field(description="Description of the event")
    mentioned_in_call: bool = Field(description="Was this mentioned in the earnings call?")
    verified: bool = Field(description="Was this verified through official sources?")
    source: str = Field(description="Source of verification")
    impact_assessment: Literal["high", "medium", "low"]


class SignificantEventDetectionResult(BaseModel):
    """Result from significant event detection agent."""
    events: List[SignificantEvent] = Field(default_factory=list)
    total_events_found: int
    verified_count: int
    confidence: float = Field(description="Overall confidence (0-1)")
    tool_validations: List[str] = Field(default_factory=list, description="Tools used for validation")


class TranscriptAnalysisAnswer(BaseModel):
    """Answer to a specific analysis question."""
    category: str
    focus_item: str
    question: str
    answer: str = Field(description="Detailed answer extracted from transcript")
    confidence: float = Field(description="Confidence in this answer (0-1)")
    relevant_quotes: List[str] = Field(default_factory=list)


class VolatilityPredictionResult(BaseModel):
    """Result from volatility prediction agent."""
    predicted_volatility: Literal["very_high", "high", "moderate", "low", "very_low"]
    volatility_score: float = Field(description="Numerical volatility prediction score (0-1)")
    transcript_insights: List[TranscriptAnalysisAnswer] = Field(default_factory=list)
    key_volatility_drivers: List[str] = Field(default_factory=list)
    sentiment_impact: str = Field(description="How sentiment impacts volatility")
    event_impact: str = Field(description="How events impact volatility")
    confidence: float = Field(description="Confidence in prediction (0-1)")
    historical_volatility: float = Field(default=0.0, description="Historical volatility from market data")
    tool_validations: List[str] = Field(default_factory=list, description="Tools used for validation")


# --- Metacognitive Models ---

class GuardrailViolation(BaseModel):
    """Record of a guardrail violation or boundary check."""
    timestamp: str
    agent: str
    guardrail_type: str
    description: str
    action_taken: str


class AgentCapability(BaseModel):
    """Capability description for a specific agent."""
    agent_name: str
    capabilities: List[str]
    limitations: List[str]
    confidence_threshold: float = Field(description="Minimum confidence required")


class FinSightSelfModel(BaseModel):
    """The metacognitive self-model for the FinSight system."""
    system_name: str = "FinSight Agent"
    version: str = "1.0"
    mission: str
    agent_capabilities: List[AgentCapability]
    operating_boundaries: List[str]
    min_confidence_for_recommendation: float = 0.7
    active_guardrails: List[str]
    guardrail_violations: List[GuardrailViolation] = Field(default_factory=list)


class MetacognitiveDecision(BaseModel):
    """The coordinator's metacognitive decision."""
    user_intent: str
    analysis_plan: List[str]
    agents_to_invoke: List[str]
    confidence: float
    reasoning: str


# --- State Models ---

class FinSightState(BaseModel):
    """Complete state for the FinSight multi-agent system."""
    user_query: str
    company_ticker: str
    transcript_path: str
    analysis_questions: List[AnalysisQuestion]
    self_model: FinSightSelfModel
    metacognitive_decision: Optional[MetacognitiveDecision] = None
    transcript_content: Optional[str] = None
    sentiment_result: Optional[SentimentAnalysisResult] = None
    event_detection_result: Optional[SignificantEventDetectionResult] = None
    volatility_result: Optional[VolatilityPredictionResult] = None
    final_report: Optional[str] = None
    guardrails_applied: List[GuardrailViolation] = Field(default_factory=list)
    errors: List[str] = Field(default_factory=list)
    
    class Config:
        arbitrary_types_allowed = True


# --- Default Configuration ---

DEFAULT_ANALYSIS_QUESTIONS = [
    AnalysisQuestion(
        category="Financial Performance",
        focus_item="Dividends",
        question="Did this company pay investors a dividend? If yes, what was the amount and frequency?",
        priority="high"
    ),
    AnalysisQuestion(
        category="Financial Performance",
        focus_item="Revenue Growth",
        question="What was the year-over-year revenue growth rate mentioned in the call?",
        priority="high"
    ),
    AnalysisQuestion(
        category="Strategic Initiatives",
        focus_item="Key Projects",
        question="What are the key projects or initiatives currently being undertaken by the company?",
        priority="high"
    ),
    AnalysisQuestion(
        category="Risk Factors",
        focus_item="Challenges",
        question="What challenges, risks, or headwinds did the management discuss?",
        priority="high"
    ),
    AnalysisQuestion(
        category="Forward Guidance",
        focus_item="Outlook",
        question="What guidance did the company provide for the next quarter or fiscal year?",
        priority="high"
    )
]


def get_default_self_model() -> FinSightSelfModel:
    """Get the default metacognitive self-model."""
    return FinSightSelfModel(
        mission="Provide comprehensive, multi-agent financial analysis of earnings calls while maintaining transparency, accuracy, and ethical boundaries",
        agent_capabilities=[
            AgentCapability(
                agent_name="Sentiment Analysis Agent",
                capabilities=[
                    "Analyze sentiment from earnings call transcripts",
                    "Correlate with market news sentiment using Tavily",
                    "Identify sentiment drivers and trends"
                ],
                limitations=[
                    "Cannot predict future sentiment with certainty",
                    "Limited to English language sources"
                ],
                confidence_threshold=0.65
            ),
            AgentCapability(
                agent_name="Significant Event Detection Agent",
                capabilities=[
                    "Identify corporate events from transcripts",
                    "Verify events against SEC filings using EDGAR",
                    "Assess event materiality and impact"
                ],
                limitations=[
                    "Cannot access all global press releases",
                    "SEC filings may have reporting delays"
                ],
                confidence_threshold=0.7
            ),
            AgentCapability(
                agent_name="Volatility Prediction Agent",
                capabilities=[
                    "Extract structured insights from transcripts",
                    "Analyze multi-modal signals",
                    "Validate predictions using yfinance market data"
                ],
                limitations=[
                    "Cannot guarantee prediction accuracy",
                    "Subject to unforeseen market shocks"
                ],
                confidence_threshold=0.6
            )
        ],
        operating_boundaries=[
            "NO personalized investment advice or stock recommendations",
            "NO guarantees about future stock performance",
            "All outputs are for educational and analytical purposes only",
            "Must disclose confidence levels and limitations"
        ],
        active_guardrails=[
            "Confidence threshold enforcement",
            "Source verification requirement",
            "Investment advice prohibition",
            "Transparent limitation disclosure"
        ]
    )

