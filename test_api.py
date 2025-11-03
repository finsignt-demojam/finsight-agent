"""
Test script for FinSight API stub
Verifies that the API can correctly parse and return analysis data
"""

from api import FinSightAPI
import json

def test_api():
    """Test all API endpoints with GOOGL ticker"""
    print("🧪 Testing FinSight API Stub")
    print("=" * 60)
    
    api = FinSightAPI()
    ticker = "GOOGL"
    
    # Test 1: Sentiment Analysis
    print("\n1️⃣  Testing Sentiment Analysis...")
    sentiment = api.analyze_sentiment(ticker)
    if sentiment:
        print(f"   ✅ Sentiment: {sentiment['sentiment']}")
        print(f"   ✅ Score: {sentiment['score']}")
        print(f"   ✅ Confidence: {sentiment['confidence']}%")
        print(f"   ✅ Key Drivers: {len(sentiment['key_drivers'])} found")
    else:
        print("   ❌ Failed to retrieve sentiment data")
    
    # Test 2: Event Detection
    print("\n2️⃣  Testing Event Detection...")
    events = api.detect_events(ticker)
    if events:
        print(f"   ✅ Total Events: {events['total_events']}")
        print(f"   ✅ Verified Events: {events['verified_events']}")
        print(f"   ✅ Confidence: {events['confidence']}%")
        print(f"   ✅ Event Details: {len(events['events'])} parsed")
    else:
        print("   ❌ Failed to retrieve event data")
    
    # Test 3: Volatility Prediction
    print("\n3️⃣  Testing Volatility Prediction...")
    volatility = api.predict_volatility(ticker)
    if volatility:
        print(f"   ✅ Predicted: {volatility['predicted_volatility']}")
        print(f"   ✅ Score: {volatility['volatility_score']}")
        print(f"   ✅ Historical: {volatility['historical_volatility']}%")
        print(f"   ✅ Confidence: {volatility['confidence']}%")
    else:
        print("   ❌ Failed to retrieve volatility data")
    
    # Test 4: Final Report
    print("\n4️⃣  Testing Final Report Generation...")
    report = api.generate_final_report(ticker)
    if report:
        print(f"   ✅ Ticker: {report['ticker']}")
        print(f"   ✅ Version: {report['version']}")
        print(f"   ✅ Events Detected: {report['events_detected']}")
        print(f"   ✅ Confidence Summary: {len(report['confidence_summary'])} agents")
    else:
        print("   ❌ Failed to retrieve final report")
    
    # Test 5: Complete Processing
    print("\n5️⃣  Testing Complete Processing...")
    results = api.process_earnings_call(ticker)
    if all([results['sentiment'], results['events'], 
            results['volatility'], results['final_report']]):
        print("   ✅ All stages completed successfully")
    else:
        print("   ❌ Some stages failed")
    
    print("\n" + "=" * 60)
    print("✅ API Testing Complete!\n")
    
    # Display sample event
    if events and len(events['events']) > 0:
        print("\n📋 Sample Event Detail:")
        print("-" * 60)
        sample_event = events['events'][0]
        print(f"Type: {sample_event['type']}")
        print(f"Description: {sample_event['description'][:100]}...")
        print(f"Impact: {sample_event['impact']}")
        print(f"Verified: {sample_event['verified']}")
    
    return True

if __name__ == "__main__":
    try:
        test_api()
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

