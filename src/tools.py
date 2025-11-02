"""
Tool implementations for FinSight Agent.
Provides access to external data sources and APIs.
"""

import os
from typing import List, Dict, Any, Optional
import yfinance as yf
from sec_edgar_downloader import Downloader
from langchain_community.tools.tavily_search import TavilySearchResults
from .config import config


class FinancialNewsSearchTool:
    """Search for financial news using Tavily."""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        if api_key:
            self.search_tool = TavilySearchResults(
                max_results=5,
                search_depth="advanced",
                api_key=api_key
            )
        else:
            self.search_tool = None
    
    def search(self, query: str, company_name: str = "") -> List[Dict[str, Any]]:
        """Search for financial news."""
        if not self.search_tool:
            return []
        
        try:
            full_query = f"{company_name} {query} financial news" if company_name else query
            results = self.search_tool.invoke(full_query)
            return results if isinstance(results, list) else []
        except Exception as e:
            print(f"Warning: News search error: {str(e)}")
            return []
    
    def get_recent_news(self, ticker: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """Get recent news for a specific ticker."""
        query = f"{ticker} earnings stock news latest"
        return self.search(query)[:max_results]
    
    def get_sentiment_news(self, ticker: str) -> List[Dict[str, Any]]:
        """Get news articles relevant for sentiment analysis."""
        query = f"{ticker} earnings sentiment market reaction analyst"
        return self.search(query)


class MarketDataTool:
    """Fetch market data from Yahoo Finance."""
    
    def get_stock_info(self, ticker: str) -> Dict[str, Any]:
        """Get basic stock information."""
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            return {
                "symbol": ticker,
                "company_name": info.get("longName", "Unknown"),
                "current_price": info.get("currentPrice", 0),
                "market_cap": info.get("marketCap", 0),
                "sector": info.get("sector", "Unknown"),
            }
        except Exception as e:
            print(f"Warning: Failed to fetch stock info: {str(e)}")
            return {"symbol": ticker, "error": "Failed to fetch"}
    
    def get_historical_volatility(self, ticker: str, period: str = "1mo") -> float:
        """Calculate historical volatility."""
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period=period)
            if not hist.empty:
                returns = hist['Close'].pct_change().dropna()
                # Annualized volatility
                return float(returns.std() * (252 ** 0.5))
            return 0.0
        except Exception as e:
            print(f"Warning: Failed to calculate volatility: {str(e)}")
            return 0.0
    
    def get_price_movement(self, ticker: str, period: str = "1mo") -> Dict[str, float]:
        """Get price movement statistics."""
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period=period)
            if not hist.empty:
                start_price = hist['Close'].iloc[0]
                end_price = hist['Close'].iloc[-1]
                change_pct = ((end_price - start_price) / start_price) * 100
                return {
                    "start_price": float(start_price),
                    "end_price": float(end_price),
                    "change_percent": float(change_pct),
                    "high": float(hist['High'].max()),
                    "low": float(hist['Low'].min()),
                }
            return {}
        except Exception as e:
            print(f"Warning: Failed to get price movement: {str(e)}")
            return {}


class SECFilingTool:
    """Download and access SEC EDGAR filings."""
    
    def __init__(self, company_name: str, email: str, download_dir: str = "./data/sec_filings"):
        self.company_name = company_name
        self.email = email
        self.download_dir = download_dir
        self.downloader = Downloader(company_name, email, download_dir)
    
    def download_recent_filings(self, ticker: str, filing_types: List[str] = None, limit: int = 5) -> Dict[str, Any]:
        """Download recent SEC filings for a ticker."""
        if filing_types is None:
            filing_types = ["10-K", "10-Q", "8-K"]
        
        results = {}
        for filing_type in filing_types:
            try:
                # Download filings
                num_downloaded = self.downloader.get(
                    filing_type,
                    ticker,
                    limit=limit,
                    download_details=True
                )
                results[filing_type] = {
                    "downloaded": num_downloaded,
                    "status": "success"
                }
            except Exception as e:
                results[filing_type] = {
                    "downloaded": 0,
                    "status": f"error: {str(e)}"
                }
        
        return results
    
    def check_recent_8k(self, ticker: str) -> List[str]:
        """Check for recent 8-K filings (material events)."""
        try:
            self.downloader.get("8-K", ticker, limit=5)
            # Return list of downloaded filing paths
            ticker_dir = os.path.join(self.download_dir, "sec-edgar-filings", ticker, "8-K")
            if os.path.exists(ticker_dir):
                return [os.path.join(ticker_dir, f) for f in os.listdir(ticker_dir)]
            return []
        except Exception as e:
            print(f"Warning: Failed to check 8-K filings: {str(e)}")
            return []


class TranscriptReaderTool:
    """Read and parse earnings call transcripts."""
    
    @staticmethod
    def read_transcript(file_path: str) -> str:
        """Read transcript from file."""
        try:
            if not os.path.exists(file_path):
                return f"Error: Transcript file not found at {file_path}"
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return content
        except Exception as e:
            return f"Error reading transcript: {str(e)}"
    
    @staticmethod
    def extract_excerpt(transcript: str, max_length: int = 3000) -> str:
        """Extract an excerpt from the transcript."""
        if len(transcript) <= max_length:
            return transcript
        return transcript[:max_length] + "..."


# Initialize global tool instances
news_search_tool = FinancialNewsSearchTool(config.api.tavily_api_key)
market_data_tool = MarketDataTool()
sec_filing_tool = SECFilingTool(
    company_name=config.sec.company_name,
    email=config.sec.email
)
transcript_reader = TranscriptReaderTool()

