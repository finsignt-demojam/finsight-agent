"""
Event Detection Agent - Identifies and validates significant corporate events.
"""

from typing import Dict, Any
from langchain_core.prompts import ChatPromptTemplate
from .base import BaseAgent
from ..models import SignificantEventDetectionResult
from ..tools import sec_filing_tool


class EventDetectionAgent(BaseAgent):
    """Agent that detects events and validates with SEC filings."""
    
    def __init__(self):
        super().__init__("Event Detection")
    
    def _validate_with_sec_filings(self, ticker: str) -> Dict[str, Any]:
        """Use SEC EDGAR downloader to validate events."""
        self.log("Validating events with SEC EDGAR filings...")
        
        validation_info = {
            "filings_checked": False,
            "filing_results": {},
            "validation_notes": []
        }
        
        try:
            # Download recent 8-K filings (material events)
            filing_results = sec_filing_tool.download_recent_filings(
                ticker,
                filing_types=["8-K", "10-Q"],
                limit=3
            )
            
            validation_info["filings_checked"] = True
            validation_info["filing_results"] = filing_results
            
            # Count successful downloads
            successful = sum(1 for r in filing_results.values() 
                           if r.get("status") == "success" and r.get("downloaded", 0) > 0)
            
            if successful > 0:
                validation_info["validation_notes"].append(
                    f"Downloaded {successful} SEC filing types for cross-reference"
                )
                self.log(f"Successfully retrieved {successful} SEC filing types")
            else:
                validation_info["validation_notes"].append(
                    "No recent SEC filings available for validation"
                )
                self.log("No SEC filings retrieved", "WARNING")
        
        except Exception as e:
            self.log(f"SEC filing error: {str(e)}", "ERROR")
            validation_info["validation_notes"].append(f"SEC filing error: {str(e)}")
        
        return validation_info
    
    def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Detect significant events and validate with SEC filings."""
        self.log("Detecting significant events...")
        
        transcript = state.get('transcript_content', '')
        ticker = state['company_ticker']
        
        # Validate with SEC filings
        sec_validation = self._validate_with_sec_filings(ticker)
        
        # Extract excerpt for analysis
        excerpt = transcript[:3000] if transcript else "No transcript available"
        
        # Build validation context
        validation_context = "\n".join(sec_validation["validation_notes"])
        
        prompt = ChatPromptTemplate.from_template(
            "Identify and analyze significant corporate events from this earnings call transcript.\n\n"
            "## Transcript Excerpt:\n{transcript}\n\n"
            "## SEC Filing Validation Context:\n{validation}\n\n"
            "## Instructions:\n"
            "Identify significant corporate events and provide:\n"
            "- events: List of events, each with:\n"
            "  - event_type: Type of event (e.g., 'merger', 'product_launch', 'earnings_beat')\n"
            "  - description: Clear description of the event\n"
            "  - mentioned_in_call: Was this explicitly mentioned in the earnings call?\n"
            "  - verified: Can this be verified through official sources?\n"
            "  - source: Source of verification (e.g., 'transcript', '8-K filing', 'both')\n"
            "  - impact_assessment: Potential impact (high/medium/low)\n"
            "- total_events_found: Total number of events identified\n"
            "- verified_count: Number of events with high confidence verification\n"
            "- confidence: Overall confidence in event detection (0-1)\n"
            "- tool_validations: List describing how SEC filings validated events"
        )
        
        try:
            structured_llm = self.llm.with_structured_output(SignificantEventDetectionResult)
            result = (prompt | structured_llm).invoke({
                "transcript": excerpt,
                "validation": validation_context
            })
            
            # Add tool validation info
            if sec_validation["filings_checked"]:
                result.tool_validations.append(
                    f"Validated events using SEC EDGAR: {sec_validation['filing_results']}"
                )
            
            self.log(f"Events detected: {result.total_events_found} "
                    f"(Verified: {result.verified_count}, Confidence: {result.confidence:.2%})")
            
            return {"event_detection_result": result}
        
        except Exception as e:
            self.log(f"Error during event detection: {str(e)}", "ERROR")
            return {
                "errors": state.get('errors', []) + [f"Event detection error: {str(e)}"]
            }

