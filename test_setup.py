#!/usr/bin/env python3
"""
Quick test script to verify FinSight Agent setup.
"""

import os
import sys

def test_imports():
    """Test that all required packages can be imported."""
    print("Testing imports...")
    
    try:
        import pydantic
        print("  ✓ pydantic")
        
        import langchain_core
        print("  ✓ langchain_core")
        
        import langchain_openai
        print("  ✓ langchain_openai")
        
        import langchain_community
        print("  ✓ langchain_community")
        
        import langgraph
        print("  ✓ langgraph")
        
        import yfinance
        print("  ✓ yfinance")
        
        from sec_edgar_downloader import Downloader
        print("  ✓ sec_edgar_downloader")
        
        from dotenv import load_dotenv
        print("  ✓ python-dotenv")
        
        print("\n✅ All imports successful!")
        return True
        
    except ImportError as e:
        print(f"\n❌ Import error: {e}")
        return False


def test_config():
    """Test configuration loading."""
    print("\nTesting configuration...")
    
    try:
        from src.config import config
        
        # Check if .env exists
        if not os.path.exists('.env'):
            print("  ⚠️  No .env file found. Copy .env.example to .env and configure it.")
            return False
        
        # Try to validate
        try:
            config.validate()
            print("  ✓ Configuration valid")
            return True
        except ValueError as e:
            print(f"  ⚠️  Configuration incomplete: {e}")
            print("  Please check your .env file")
            return False
            
    except Exception as e:
        print(f"  ❌ Configuration error: {e}")
        return False


def test_modules():
    """Test that all modules can be imported."""
    print("\nTesting FinSight modules...")
    
    try:
        from src import config, models, tools, orchestrator
        print("  ✓ Core modules")
        
        from src.agents import (
            CoordinatorAgent,
            SentimentAnalysisAgent,
            EventDetectionAgent,
            VolatilityPredictionAgent
        )
        print("  ✓ Agent modules")
        
        print("\n✅ All modules loaded successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ Module error: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("="*60)
    print("FinSight Agent - Setup Test")
    print("="*60 + "\n")
    
    results = []
    
    results.append(("Imports", test_imports()))
    results.append(("Modules", test_modules()))
    results.append(("Configuration", test_config()))
    
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {status}: {test_name}")
    
    all_passed = all(result for _, result in results)
    
    if all_passed:
        print("\n🎉 FinSight Agent is ready to use!")
        print("\nNext steps:")
        print("  1. Ensure .env is configured with your API keys")
        print("  2. Run: python -m src.main --help")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please resolve the issues above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())

