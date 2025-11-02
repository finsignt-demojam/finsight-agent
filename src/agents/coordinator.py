"""
Coordinator Agent - Orchestrates the multi-agent analysis workflow.
"""

from typing import Dict, Any
from langchain_core.prompts import ChatPromptTemplate
from .base import BaseAgent
from ..models import MetacognitiveDecision


class CoordinatorAgent(BaseAgent):
    """Metacognitive coordinator that plans and orchestrates analysis."""
    
    def __init__(self):
        super().__init__("Coordinator")
    
    def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Create analysis plan and coordinate agents."""
        self.log("Planning comprehensive analysis...")
        
        prompt = ChatPromptTemplate.from_template(
            "You are the metacognitive coordinator for FinSight, a financial analysis system. "
            "Analyze the user query and create a detailed analysis plan.\n\n"
            "User Query: {query}\n"
            "Company Ticker: {ticker}\n\n"
            "Determine:\n"
            "1. User's intent and objectives\n"
            "2. Detailed analysis steps needed\n"
            "3. Which specialized agents to invoke (sentiment_analysis, event_detection, volatility_prediction)\n"
            "4. Your confidence level (0-1) in understanding the request\n"
            "5. Reasoning behind your plan\n\n"
            "Provide structured output with fields: user_intent, analysis_plan (list), "
            "agents_to_invoke (list), confidence, reasoning"
        )
        
        try:
            structured_llm = self.llm.with_structured_output(MetacognitiveDecision)
            decision = (prompt | structured_llm).invoke({
                "query": state['user_query'],
                "ticker": state['company_ticker']
            })
            
            self.log(f"Analysis plan created - Confidence: {decision.confidence:.2f}")
            self.log(f"Intent: {decision.user_intent}")
            self.log(f"Agents to invoke: {', '.join(decision.agents_to_invoke)}")
            
            return {
                "metacognitive_decision": decision,
                "guardrails_applied": state.get('guardrails_applied', [])
            }
        
        except Exception as e:
            self.log(f"Error during planning: {str(e)}", "ERROR")
            return {
                "errors": state.get('errors', []) + [f"Coordinator error: {str(e)}"]
            }

