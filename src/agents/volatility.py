"""
Volatility Prediction Agent - Predicts stock volatility using multi-modal analysis.
"""

from typing import Dict, Any, List
from langchain_core.prompts import ChatPromptTemplate
from .base import BaseAgent
from ..models import VolatilityPredictionResult, TranscriptAnalysisAnswer
from ..tools import market_data_tool


class VolatilityPredictionAgent(BaseAgent):
    """Agent that predicts volatility using transcript analysis and market data validation."""
    
    def __init__(self):
        super().__init__("Volatility Prediction")
    
    def _validate_with_market_data(self, ticker: str) -> Dict[str, Any]:
        """Use yfinance to gather market data for validation."""
        self.log("Validating with market data via yfinance...")
        
        validation_info = {
            "historical_volatility": 0.0,
            "price_movement": {},
            "stock_info": {},
            "validation_notes": []
        }
        
        try:
            # Get historical volatility
            hist_vol = market_data_tool.get_historical_volatility(ticker, period="1mo")
            validation_info["historical_volatility"] = hist_vol
            self.log(f"Historical volatility: {hist_vol:.2%}")
            
            # Get price movement
            price_movement = market_data_tool.get_price_movement(ticker, period="1mo")
            validation_info["price_movement"] = price_movement
            
            if price_movement:
                change = price_movement.get("change_percent", 0)
                self.log(f"Price movement: {change:.2f}%")
                validation_info["validation_notes"].append(
                    f"1-month price change: {change:.2f}%, volatility: {hist_vol:.2%}"
                )
            
            # Get stock info
            stock_info = market_data_tool.get_stock_info(ticker)
            validation_info["stock_info"] = stock_info
            
        except Exception as e:
            self.log(f"Market data error: {str(e)}", "ERROR")
            validation_info["validation_notes"].append(f"Market data error: {str(e)}")
        
        return validation_info
    
    def _answer_analysis_questions(self, transcript: str, questions: List) -> List[TranscriptAnalysisAnswer]:
        """Answer analysis questions from the transcript."""
        self.log(f"Answering {len(questions)} analysis questions...")
        
        insights = []
        excerpt = transcript[:4000] if transcript else "No transcript available"
        
        for q in questions[:5]:  # Limit to first 5 questions
            prompt = ChatPromptTemplate.from_template(
                "Answer this specific question from the earnings call transcript.\n\n"
                "## Question:\n{question}\n\n"
                "## Transcript Excerpt:\n{transcript}\n\n"
                "## Instructions:\n"
                "Provide:\n"
                "- category: Question category\n"
                "- focus_item: Focus area\n"
                "- question: The question being answered\n"
                "- answer: Detailed answer extracted from transcript\n"
                "- confidence: Confidence in this answer (0-1)\n"
                "- relevant_quotes: List of relevant quotes from transcript supporting this answer"
            )
            
            try:
                structured_llm = self.llm.with_structured_output(TranscriptAnalysisAnswer)
                answer = (prompt | structured_llm).invoke({
                    "question": q.question,
                    "transcript": excerpt
                })
                insights.append(answer)
                self.log(f"Answered: {q.focus_item} (Confidence: {answer.confidence:.2%})")
            except Exception as e:
                self.log(f"Question error for '{q.focus_item}': {str(e)}", "WARNING")
        
        return insights
    
    def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Predict volatility using transcript insights and market data."""
        self.log("Predicting volatility...")
        
        transcript = state.get('transcript_content', '')
        ticker = state['company_ticker']
        analysis_questions = state.get('analysis_questions', [])
        
        # Validate with market data
        market_validation = self._validate_with_market_data(ticker)
        
        # Answer analysis questions
        insights = self._answer_analysis_questions(transcript, analysis_questions)
        
        # Get sentiment and events for context
        sentiment_summary = "Unknown"
        if state.get('sentiment_result'):
            sent = state['sentiment_result']
            sentiment_summary = f"{sent.overall_sentiment} (score: {sent.sentiment_score:.2f})"
        
        events_summary = "Unknown"
        if state.get('event_detection_result'):
            events = state['event_detection_result']
            events_summary = f"{events.total_events_found} events ({events.verified_count} verified)"
        
        # Build validation context
        validation_context = "\n".join(market_validation["validation_notes"])
        
        prompt = ChatPromptTemplate.from_template(
            "Predict stock volatility based on comprehensive multi-modal analysis.\n\n"
            "## Market Data:\n"
            "Historical Volatility (1-month): {hist_vol:.2%}\n"
            "Price Movement: {price_movement}\n\n"
            "## Sentiment Analysis:\n{sentiment}\n\n"
            "## Significant Events:\n{events}\n\n"
            "## Market Validation:\n{validation}\n\n"
            "## Instructions:\n"
            "Predict stock volatility including:\n"
            "- predicted_volatility: Choose from very_high/high/moderate/low/very_low\n"
            "- volatility_score: Numerical score (0-1, higher = more volatile)\n"
            "- transcript_insights: Will be populated separately\n"
            "- key_volatility_drivers: Main factors contributing to predicted volatility\n"
            "- sentiment_impact: How sentiment analysis impacts volatility prediction\n"
            "- event_impact: How significant events impact volatility prediction\n"
            "- confidence: Confidence in volatility prediction (0-1)\n"
            "- historical_volatility: The historical volatility value\n"
            "- tool_validations: List describing how market data validated predictions"
        )
        
        try:
            structured_llm = self.llm.with_structured_output(VolatilityPredictionResult)
            result = (prompt | structured_llm).invoke({
                "hist_vol": market_validation["historical_volatility"],
                "price_movement": str(market_validation["price_movement"]),
                "sentiment": sentiment_summary,
                "events": events_summary,
                "validation": validation_context
            })
            
            # Add transcript insights
            result.transcript_insights = insights
            result.historical_volatility = market_validation["historical_volatility"]
            
            # Add tool validation info
            if market_validation["validation_notes"]:
                result.tool_validations.append(
                    f"Validated with yfinance: {', '.join(market_validation['validation_notes'])}"
                )
            
            self.log(f"Volatility: {result.predicted_volatility} "
                    f"(Score: {result.volatility_score:.2f}, Confidence: {result.confidence:.2%})")
            
            return {"volatility_result": result}
        
        except Exception as e:
            self.log(f"Error during volatility prediction: {str(e)}", "ERROR")
            return {
                "errors": state.get('errors', []) + [f"Volatility prediction error: {str(e)}"]
            }

