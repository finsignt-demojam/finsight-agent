#!/bin/bash
# Quick test script for FinSight Agent

echo "======================================================================"
echo "FinSight Agent - Quick Test Script"
echo "======================================================================"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ .env file not found!"
    echo ""
    echo "Please create .env file from .env.example:"
    echo "  cp .env.example .env"
    echo ""
    echo "Then edit .env with your API keys:"
    echo "  - SCW_DEFAULT_PROJECT_ID"
    echo "  - SCW_SECRET_KEY"
    echo "  - TAVILY_API_KEY"
    echo ""
    exit 1
fi

echo "✅ .env file found"
echo ""

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  Virtual environment not activated"
    echo ""
    echo "Activate it with:"
    echo "  source .venv/bin/activate    # On macOS/Linux"
    echo "  .venv\\Scripts\\activate      # On Windows"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Run setup test
echo "Running setup test..."
echo ""
python test_setup.py

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Setup test failed. Please fix issues above."
    exit 1
fi

echo ""
echo "======================================================================"
echo "Setup verified! You can now run the analysis."
echo "======================================================================"
echo ""
echo "Quick start commands:"
echo ""
echo "1. Run demo (interactive):"
echo "   python demo.py"
echo ""
echo "2. Run CLI analysis:"
echo "   python -m src.main \\"
echo "     --transcript data/input/Alphabet_2025_Q1_Earnings_Call_complete_transcript.txt \\"
echo "     --ticker GOOGL"
echo ""
echo "3. See all options:"
echo "   python -m src.main --help"
echo ""
echo "4. View examples:"
echo "   python examples.py"
echo ""
echo "Reports will be saved to: data/output/"
echo ""

