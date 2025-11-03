#!/bin/bash
# FinSight AI Agent - Streamlit Launcher

echo "🚀 Starting FinSight AI Agent Streamlit Interface..."
echo "---------------------------------------------------"

# Check if streamlit is installed
if ! command -v streamlit &> /dev/null
then
    echo "❌ Streamlit is not installed."
    echo "Installing dependencies..."
    pip install -r requirements.txt
fi

# Launch streamlit
echo "✅ Launching application on http://localhost:8501"
echo ""
streamlit run app.py

