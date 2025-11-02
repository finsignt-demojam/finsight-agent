"""
Example script demonstrating how to use FinSight Agent programmatically.
"""

from src.orchestrator import FinSightOrchestrator
from src.config import config

def example_basic_analysis():
    """Basic usage example."""
    print("Example 1: Basic Analysis")
    print("-" * 60)
    
    # Initialize orchestrator
    orchestrator = FinSightOrchestrator()
    
    # Run analysis
    result = orchestrator.run_analysis(
        transcript_path="data/input/GOOG_2025_Q3_Earnings_Transcript.pdf",
        ticker="GOOGL"
    )
    
    print(f"\nAnalysis complete! Check {config.paths.output_dir} for reports.")
    return result


def example_custom_query():
    """Example with custom query."""
    print("\nExample 2: Custom Query Analysis")
    print("-" * 60)
    
    orchestrator = FinSightOrchestrator()
    
    result = orchestrator.run_analysis(
        transcript_path="data/input/GOOG_2025_Q3_Earnings_Transcript.pdf",
        ticker="GOOGL",
        user_query="Focus on AI initiatives and their impact on revenue growth"
    )
    
    return result


def example_accessing_results():
    """Example of accessing individual agent results."""
    print("\nExample 3: Accessing Results Programmatically")
    print("-" * 60)
    
    orchestrator = FinSightOrchestrator()
    
    result = orchestrator.run_analysis(
        transcript_path="data/input/GOOG_2025_Q3_Earnings_Transcript.pdf",
        ticker="GOOGL"
    )
    
    # Access sentiment results
    if result.get('sentiment_result'):
        sent = result['sentiment_result']
        print(f"\nSentiment: {sent.overall_sentiment}")
        print(f"Score: {sent.sentiment_score:.2f}")
        print(f"Confidence: {sent.confidence:.2%}")
    
    # Access event results
    if result.get('event_detection_result'):
        events = result['event_detection_result']
        print(f"\nEvents detected: {events.total_events_found}")
        print(f"Verified: {events.verified_count}")
    
    # Access volatility results
    if result.get('volatility_result'):
        vol = result['volatility_result']
        print(f"\nPredicted volatility: {vol.predicted_volatility}")
        print(f"Historical volatility: {vol.historical_volatility:.2%}")
    
    return result


def main():
    """Run examples."""
    print("="*60)
    print("FinSight Agent - Usage Examples")
    print("="*60 + "\n")
    
    try:
        # Validate configuration
        config.validate()
        
        # Run examples (uncomment as needed)
        # example_basic_analysis()
        # example_custom_query()
        # example_accessing_results()
        
        print("\n💡 Tip: Uncomment the example functions in this script to try them!")
        print("   Or use the CLI: python -m src.main --help")
        
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        print("\nPlease ensure your .env file is properly configured.")
        print("Required variables:")
        print("  - SCW_DEFAULT_PROJECT_ID")
        print("  - SCW_SECRET_KEY")
        print("  - TAVILY_API_KEY")


if __name__ == "__main__":
    main()

