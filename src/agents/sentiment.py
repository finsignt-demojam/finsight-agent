"""
Sentiment Analysis Agent - Analyzes sentiment from earnings calls and market news.
"""

from typing import Dict, Any, List
from langchain_core.prompts import ChatPromptTemplate
from .base import BaseAgent
from ..models import SentimentAnalysisResult
from ..tools import news_search_tool


class SentimentAnalysisAgent(BaseAgent):
    """Agent that analyzes sentiment using transcript and news validation."""
    
    def __init__(self):
        super().__init__("Sentiment Analysis")
    
    def _gather_news_context(self, ticker: str) -> tuple[List[str], List[Dict[str, Any]]]:
        """Use Tavily to gather recent news for sentiment validation."""
        self.log("Gathering news context via Tavily...")
        
        news_headlines = []
        news_data = []
        
        try:
            # Get sentiment-relevant news
            results = news_search_tool.get_sentiment_news(ticker)
            if results:
                news_headlines = [r.get('title', '')[:100] for r in results[:5]]
                news_data = results[:5]
                self.log(f"Retrieved {len(news_headlines)} news articles")
            else:
                self.log("No news results returned", "WARNING")
        except Exception as e:
            self.log(f"News search error: {str(e)}", "ERROR")
        
        return news_headlines, news_data
    
    def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze sentiment from transcript and validate with news."""
        self.log("Analyzing sentiment...")
        
        transcript = state.get('transcript_content', '')
        ticker = state['company_ticker']
        
        # Gather news context for validation
        news_headlines, news_data = self._gather_news_context(ticker)
        
        # Extract excerpt for analysis
        excerpt = transcript[:3000] if transcript else "No transcript available"
        
        # Build context with news
        news_context = "\n".join(news_headlines) if news_headlines else "No recent news available"
        
        prompt = ChatPromptTemplate.from_template(
            "Analyze the sentiment from this earnings call transcript and validate with recent market news.\n\n"
            "## Transcript Excerpt:\n{transcript}\n\n"
            "## Recent Market News:\n{news}\n\n"
            "## Instructions:\n"
            "Provide a comprehensive sentiment analysis including:\n"
            "- overall_sentiment: Choose from very_positive/positive/neutral/negative/very_negative\n"
            "- sentiment_score: Numerical score from -1.0 (very negative) to 1.0 (very positive)\n"
            "- market_sentiment: Summary of broader market sentiment based on news\n"
            "- key_sentiment_drivers: List of key topics driving the sentiment\n"
            "- news_headlines: List of relevant news headlines analyzed\n"
            "- confidence: Your confidence level (0-1) in this assessment\n"
            "- tool_validations: List describing how news data validated or contradicted transcript sentiment"
        )
        
        try:
            structured_llm = self.llm.with_structured_output(SentimentAnalysisResult)
            result = (prompt | structured_llm).invoke({
                "transcript": excerpt,
                "news": news_context
            })
            
            # Add tool validation info
            if news_headlines:
                result.news_headlines = news_headlines
                result.tool_validations.append(
                    f"Validated sentiment using {len(news_headlines)} news articles from Tavily"
                )
            
            self.log(f"Sentiment: {result.overall_sentiment} (Score: {result.sentiment_score:.2f}, "
                    f"Confidence: {result.confidence:.2%})")
            
            return {"sentiment_result": result}
        
        except Exception as e:
            self.log(f"Error during sentiment analysis: {str(e)}", "ERROR")
            return {
                "errors": state.get('errors', []) + [f"Sentiment analysis error: {str(e)}"]
            }

