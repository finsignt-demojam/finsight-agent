#!/usr/bin/env python3
"""
Demo script showing FinSight Agent in action.
This script runs a complete analysis on a sample transcript.
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.orchestrator import FinSightOrchestrator
from src.config import config


def print_banner():
    """Print welcome banner."""
    print("\n" + "="*80)
    print("    FinSight Agent - Multi-Agent Financial Analysis System")
    print("="*80)
    print("\n🎯 Demonstration Mode\n")
    print("This demo will run a complete analysis on an earnings call transcript,")
    print("showcasing all specialized agents and their tool usage.\n")


def check_prerequisites():
    """Check if all prerequisites are met."""
    print("📋 Checking prerequisites...\n")
    
    issues = []
    
    # Check .env file
    if not os.path.exists('.env'):
        issues.append("❌ .env file not found (copy .env.example and configure)")
    else:
        print("✅ .env file exists")
    
    # Check configuration
    try:
        config.validate()
        print("✅ Configuration valid")
    except ValueError as e:
        issues.append(f"❌ Configuration error: {e}")
    
    # Check for transcript files
    input_dir = Path("data/input")
    transcripts = list(input_dir.glob("*.txt"))
    if not transcripts:
        issues.append("❌ No transcript files found in data/input/")
    else:
        print(f"✅ Found {len(transcripts)} transcript(s)")
    
    if issues:
        print("\n⚠️  Issues found:")
        for issue in issues:
            print(f"  {issue}")
        print("\nPlease resolve these issues before running the demo.")
        return False, None
    
    return True, transcripts[0] if transcripts else None


def run_demo(transcript_path: Path):
    """Run the demo analysis."""
    print(f"\n📄 Using transcript: {transcript_path.name}")
    print(f"📊 Ticker: GOOGL\n")
    
    print("="*80)
    print("Starting Multi-Agent Analysis Pipeline")
    print("="*80)
    
    # Initialize orchestrator
    orchestrator = FinSightOrchestrator()
    
    # Run analysis with detailed query
    result = orchestrator.run_analysis(
        transcript_path=str(transcript_path),
        ticker="GOOGL",
        user_query=(
            "Provide comprehensive financial analysis including sentiment assessment, "
            "significant corporate events, and volatility prediction. "
            "Validate findings using external data sources."
        )
    )
    
    return result


def display_results(result):
    """Display summary of results."""
    print("\n" + "="*80)
    print("Analysis Results Summary")
    print("="*80 + "\n")
    
    # Sentiment results
    if result.get('sentiment_result'):
        sent = result['sentiment_result']
        print("😊 SENTIMENT ANALYSIS")
        print(f"   Overall: {sent.overall_sentiment.upper()}")
        print(f"   Score: {sent.sentiment_score:.2f} (range: -1.0 to 1.0)")
        print(f"   Confidence: {sent.confidence:.2%}")
        print(f"   News articles analyzed: {len(sent.news_headlines)}")
        print(f"   Tool validations: {len(sent.tool_validations)}")
    
    print()
    
    # Event results
    if result.get('event_detection_result'):
        events = result['event_detection_result']
        print("🔍 EVENT DETECTION")
        print(f"   Events detected: {events.total_events_found}")
        print(f"   Events verified: {events.verified_count}")
        print(f"   Confidence: {events.confidence:.2%}")
        print(f"   Tool validations: {len(events.tool_validations)}")
    
    print()
    
    # Volatility results
    if result.get('volatility_result'):
        vol = result['volatility_result']
        print("📊 VOLATILITY PREDICTION")
        print(f"   Predicted: {vol.predicted_volatility.upper()}")
        print(f"   Score: {vol.volatility_score:.2f} (range: 0.0 to 1.0)")
        print(f"   Historical volatility: {vol.historical_volatility:.2%}")
        print(f"   Confidence: {vol.confidence:.2%}")
        print(f"   Transcript insights: {len(vol.transcript_insights)}")
        print(f"   Tool validations: {len(vol.tool_validations)}")
    
    print()
    
    # Guardrails
    guardrails = result.get('guardrails_applied', [])
    print("🛡️  GUARDRAILS")
    print(f"   Checks performed: {len(guardrails)}")
    if guardrails:
        print("   Violations detected:")
        for g in guardrails:
            print(f"     - {g.guardrail_type} ({g.agent})")
    else:
        print("   ✅ All confidence thresholds met")
    
    print()
    
    # Output files
    print("📁 OUTPUT FILES")
    output_dir = Path(config.paths.output_dir)
    if output_dir.exists():
        reports = list(output_dir.glob("*.md"))
        recent_reports = sorted(reports, key=lambda x: x.stat().st_mtime, reverse=True)[:4]
        for report in recent_reports:
            print(f"   📄 {report.name}")
    
    print("\n" + "="*80)


def main():
    """Main demo function."""
    print_banner()
    
    # Check prerequisites
    ready, transcript_path = check_prerequisites()
    if not ready:
        sys.exit(1)
    
    print("\n" + "="*80)
    input("\nPress ENTER to start the analysis...")
    print("="*80)
    
    try:
        # Run demo
        result = run_demo(transcript_path)
        
        # Display results
        display_results(result)
        
        print("\n✅ Demo completed successfully!")
        print(f"\n💡 View detailed reports in: {config.paths.output_dir}")
        print("\n📚 For more information:")
        print("   - See README.md for architecture details")
        print("   - See QUICKSTART.md for usage guide")
        print("   - Run: python -m src.main --help")
        
        return 0
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user")
        return 130
    
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())

