"""
Main entry point for FinSight Agent.
Run multi-agent financial analysis on earnings call transcripts.
"""

import sys
import argparse
from pathlib import Path

from .config import config
from .orchestrator import FinSightOrchestrator


def validate_inputs(transcript_path: str, ticker: str) -> bool:
    """Validate input parameters."""
    if not Path(transcript_path).exists():
        print(f"❌ Error: Transcript file not found: {transcript_path}")
        return False
    
    if not ticker or len(ticker) > 10:
        print(f"❌ Error: Invalid ticker symbol: {ticker}")
        return False
    
    return True


def main():
    """Main function to run FinSight Agent."""
    parser = argparse.ArgumentParser(
        description="FinSight Agent: Metacognitive Multi-Agent Financial Analysis System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example usage:
  python -m src.main --transcript data/input/transcript.txt --ticker GOOGL
  python -m src.main -t data/input/transcript.txt -s GOOGL --query "Analyze sentiment"
        """
    )
    
    parser.add_argument(
        '-t', '--transcript',
        type=str,
        required=True,
        help='Path to earnings call transcript file (.txt format)'
    )
    
    parser.add_argument(
        '-s', '--ticker',
        type=str,
        required=True,
        help='Company ticker symbol (e.g., GOOGL, AAPL, MSFT)'
    )
    
    parser.add_argument(
        '-q', '--query',
        type=str,
        default=None,
        help='Optional: Custom analysis query (default: comprehensive analysis)'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        default=None,
        help='Optional: Output directory for reports (default: ./data/output)'
    )
    
    args = parser.parse_args()
    
    # Validate configuration
    try:
        config.validate()
        print("✅ Configuration validated")
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        print("\nPlease ensure the following environment variables are set:")
        print("  - SCW_DEFAULT_PROJECT_ID")
        print("  - SCW_SECRET_KEY")
        print("  - TAVILY_API_KEY")
        sys.exit(1)
    
    # Validate inputs
    if not validate_inputs(args.transcript, args.ticker):
        sys.exit(1)
    
    # Update output directory if specified
    if args.output:
        config.paths.output_dir = args.output
    
    # Initialize orchestrator
    print("\n🔧 Initializing FinSight Agent...")
    orchestrator = FinSightOrchestrator()
    
    # Run analysis
    try:
        result = orchestrator.run_analysis(
            transcript_path=args.transcript,
            ticker=args.ticker.upper(),
            user_query=args.query
        )
        
        # Display summary
        print("\n📈 Analysis Summary:")
        print(f"  - Sentiment: {result.get('sentiment_result').overall_sentiment if result.get('sentiment_result') else 'N/A'}")
        print(f"  - Events: {result.get('event_detection_result').total_events_found if result.get('event_detection_result') else 0}")
        print(f"  - Volatility: {result.get('volatility_result').predicted_volatility if result.get('volatility_result') else 'N/A'}")
        print(f"\n📁 Reports saved to: {config.paths.output_dir}")
        
        return 0
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Analysis interrupted by user")
        return 130
    
    except Exception as e:
        print(f"\n❌ Fatal error: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())

