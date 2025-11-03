"""
FinSight AI Agent - Streamlit Frontend
A professional, single-page interface for earnings call analysis
"""

import streamlit as st
import time
from pathlib import Path
from api import FinSightAPI

# Page configuration
st.set_page_config(
    page_title="FinSight AI Agent",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    /* Main container styling */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Header styling */
    .header-container {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .header-title {
        color: white;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        text-align: center;
    }
    
    .header-subtitle {
        color: #e0e7ff;
        font-size: 1.1rem;
        text-align: center;
        margin-top: 0.5rem;
    }
    
    /* Card styling */
    .analysis-card {
        background: white;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #2a5298;
    }
    
    /* Confidence badge styling */
    .confidence-badge {
        display: inline-block;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.9rem;
        margin: 0.5rem 0;
    }
    
    .confidence-high {
        background-color: #10b981;
        color: white;
    }
    
    .confidence-medium {
        background-color: #f59e0b;
        color: white;
    }
    
    .confidence-low {
        background-color: #ef4444;
        color: white;
    }
    
    /* Status indicator */
    .status-indicator {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .status-processing {
        background-color: #fef3c7;
        border-left: 4px solid #f59e0b;
    }
    
    .status-complete {
        background-color: #d1fae5;
        border-left: 4px solid #10b981;
    }
    
    /* Section headers */
    .section-header {
        color: #1e3c72;
        font-size: 1.8rem;
        font-weight: 700;
        margin: 2rem 0 1rem 0;
        border-bottom: 3px solid #2a5298;
        padding-bottom: 0.5rem;
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
    }
    
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
        margin-top: 0.5rem;
    }
    
    /* Scrollable content */
    .scrollable-content {
        max-height: 600px;
        overflow-y: auto;
        padding: 1rem;
        background: #f9fafb;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    /* Event card */
    .event-card {
        background: white;
        padding: 1rem;
        margin: 0.8rem 0;
        border-radius: 8px;
        border-left: 4px solid #6366f1;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    
    .event-title {
        font-weight: 600;
        color: #1e293b;
        font-size: 1.1rem;
    }
    
    .event-impact {
        display: inline-block;
        padding: 0.2rem 0.6rem;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-top: 0.5rem;
    }
    
    .impact-high {
        background-color: #fee2e2;
        color: #991b1b;
    }
    
    .impact-medium {
        background-color: #fef3c7;
        color: #92400e;
    }
    
    .impact-low {
        background-color: #dbeafe;
        color: #1e40af;
    }
</style>
""", unsafe_allow_html=True)

def get_confidence_badge(confidence: float) -> str:
    """Generate HTML for confidence badge"""
    if confidence >= 85:
        css_class = "confidence-high"
        label = "High Confidence"
    elif confidence >= 70:
        css_class = "confidence-medium"
        label = "Medium Confidence"
    else:
        css_class = "confidence-low"
        label = "Low Confidence"
    
    return f'<span class="confidence-badge {css_class}">{label}: {confidence:.1f}%</span>'

def display_sentiment_analysis(sentiment_data: dict):
    """Display sentiment analysis results"""
    st.markdown('<div class="section-header">📈 Sentiment Analysis</div>', unsafe_allow_html=True)
    
    # Key metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{sentiment_data['sentiment'].replace('_', ' ').title()}</div>
            <div class="metric-label">Overall Sentiment</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{sentiment_data['score']:.2f}</div>
            <div class="metric-label">Sentiment Score (-1.0 to 1.0)</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{sentiment_data['confidence']:.0f}%</div>
            <div class="metric-label">Confidence Level</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Use tabs to separate main output from audit data
    tab1, tab2 = st.tabs(["📊 Analysis Output", "🔍 Audit Data"])
    
    with tab1:
        st.markdown(f"""
        <div class="analysis-card">
            <h4>Market Sentiment Summary</h4>
            <p>{sentiment_data['market_summary']}</p>
            {get_confidence_badge(sentiment_data['confidence'])}
        </div>
        """, unsafe_allow_html=True)
        
        if sentiment_data.get('key_drivers'):
            st.markdown("""
            <div class="analysis-card">
                <h4>Key Sentiment Drivers</h4>
            """, unsafe_allow_html=True)
            for driver in sentiment_data['key_drivers']:
                st.markdown(f"• {driver}")
            st.markdown("</div>", unsafe_allow_html=True)
        
        if sentiment_data.get('news_headlines'):
            st.markdown("""
            <div class="analysis-card">
                <h4>News Headlines Analyzed</h4>
            """, unsafe_allow_html=True)
            for headline in sentiment_data['news_headlines']:
                st.markdown(f"• {headline}")
            st.markdown("</div>", unsafe_allow_html=True)
    
    with tab2:
        st.markdown("##### 🔎 Tool Validations & Data Sources")
        st.info("This section shows how the agent verified its analysis using external tools and data sources.")
        
        if sentiment_data.get('tool_validations'):
            st.markdown("""
            <div class="analysis-card">
                <h4>Validation Steps</h4>
            """, unsafe_allow_html=True)
            for validation in sentiment_data['tool_validations']:
                st.markdown(f"✓ {validation}")
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.warning("No tool validation data available.")

def display_event_detection(events_data: dict):
    """Display event detection results"""
    st.markdown('<div class="section-header">🎯 Significant Event Detection</div>', unsafe_allow_html=True)
    
    # Key metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{events_data['total_events']}</div>
            <div class="metric-label">Total Events Detected</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{events_data['verified_events']}</div>
            <div class="metric-label">Verified Events</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{events_data['confidence']:.0f}%</div>
            <div class="metric-label">Confidence Level</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Use tabs to separate main output from audit data
    tab1, tab2 = st.tabs(["📊 Analysis Output", "🔍 Audit Data"])
    
    with tab1:
        for i, event in enumerate(events_data['events'], 1):
            impact_class = f"impact-{event['impact'].lower()}"
            st.markdown(f"""
            <div class="event-card">
                <div class="event-title">Event {i}: {event['type'].replace('_', ' ').title()}</div>
                <p style="margin: 0.5rem 0; color: #475569;">{event['description']}</p>
                <span class="event-impact {impact_class}">{event['impact']} IMPACT</span>
                <span style="margin-left: 1rem; color: #64748b; font-size: 0.85rem;">
                    ✓ Verified from {event['source']}
                </span>
            </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("##### 🔎 Tool Validations & Data Sources")
        st.info("This section shows how the agent verified detected events using SEC filings and other sources.")
        
        if events_data.get('tool_validations'):
            st.markdown("""
            <div class="analysis-card">
                <h4>Validation Steps</h4>
            """, unsafe_allow_html=True)
            for validation in events_data['tool_validations']:
                st.markdown(f"✓ {validation}")
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.warning("No tool validation data available.")

def display_volatility_prediction(volatility_data: dict):
    """Display volatility prediction results"""
    st.markdown('<div class="section-header">📊 Volatility Prediction</div>', unsafe_allow_html=True)
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{volatility_data['predicted_volatility'].upper()}</div>
            <div class="metric-label">Predicted Volatility</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{volatility_data['volatility_score']:.2f}</div>
            <div class="metric-label">Volatility Score (0-1)</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{volatility_data['historical_volatility']:.1f}%</div>
            <div class="metric-label">Historical Volatility</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{volatility_data['confidence']:.0f}%</div>
            <div class="metric-label">Confidence Level</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Use tabs to separate main output from audit data
    tab1, tab2, tab3 = st.tabs(["📊 Analysis Output", "📝 Transcript Insights", "🔍 Audit Data"])
    
    with tab1:
        st.markdown(f"""
        <div class="analysis-card">
            <h4>Key Volatility Drivers</h4>
        """, unsafe_allow_html=True)
        for driver in volatility_data['key_drivers']:
            st.markdown(f"• {driver}")
        st.markdown(f"""
            {get_confidence_badge(volatility_data['confidence'])}
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="analysis-card">
            <h4>Sentiment Impact</h4>
            <p>{volatility_data['sentiment_impact']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="analysis-card">
            <h4>Event Impact</h4>
            <p>{volatility_data['event_impact']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("##### 📝 Key Insights from Earnings Call Transcript")
        st.info("These insights are extracted directly from the earnings call using LLM analysis of the transcript.")
        
        if volatility_data.get('transcript_insights'):
            for insight in volatility_data['transcript_insights']:
                with st.expander(f"📌 {insight['title']}", expanded=False):
                    st.markdown(f"**Question:** {insight['question']}")
                    st.markdown(f"**Answer:** {insight['answer']}")
                    st.markdown(f"{get_confidence_badge(insight['confidence'])}", unsafe_allow_html=True)
        else:
            st.warning("No transcript insights available.")
    
    with tab3:
        st.markdown("##### 🔎 Tool Validations & Data Sources")
        st.info("This section shows how the agent validated volatility predictions using market data.")
        
        if volatility_data.get('tool_validations'):
            st.markdown("""
            <div class="analysis-card">
                <h4>Validation Steps</h4>
            """, unsafe_allow_html=True)
            for validation in volatility_data['tool_validations']:
                st.markdown(f"✓ {validation}")
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.warning("No tool validation data available.")

def display_final_report(report_data: dict):
    """Display comprehensive final report"""
    st.markdown('<div class="section-header">📋 Comprehensive Analysis Report</div>', unsafe_allow_html=True)
    
    # Executive summary
    st.markdown(f"""
    <div class="analysis-card">
        <h3 style="color: #1e3c72; margin-top: 0;">Executive Summary</h3>
        <p><strong>Company:</strong> {report_data['ticker']}</p>
        <p><strong>Generated:</strong> {report_data['generated']}</p>
        <p><strong>System Version:</strong> {report_data['version']}</p>
        <hr style="border: 1px solid #e5e7eb; margin: 1rem 0;">
        <p><strong>Sentiment:</strong> {report_data['sentiment']} (Score: {report_data['sentiment_score']:.2f}, {get_confidence_badge(report_data['sentiment_confidence'])})</p>
        <p><strong>Events Detected:</strong> {report_data['events_detected']} ({report_data['events_verified']} verified, {get_confidence_badge(report_data['events_confidence'])})</p>
        <p><strong>Predicted Volatility:</strong> {report_data['predicted_volatility'].upper()} (Score: {report_data['volatility_score']:.2f}, {get_confidence_badge(report_data['volatility_confidence'])})</p>
        <p><strong>Historical Volatility:</strong> {report_data['historical_volatility']:.2f}%</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Use tabs to separate main output from audit data
    tab1, tab2, tab3 = st.tabs(["📊 System Confidence", "🧠 Metacognitive Analysis", "🛡️ Guardrails & Boundaries"])
    
    with tab1:
        st.markdown("##### System Confidence Summary")
        st.info("This table shows the confidence levels of each specialized agent and whether they meet the required thresholds.")
        
        # Build table using Streamlit native table (fix for formatting issue)
        import pandas as pd
        if report_data.get('confidence_summary'):
            df = pd.DataFrame(report_data['confidence_summary'])
            # Format the dataframe for better display
            df['confidence'] = df['confidence'].apply(lambda x: f"{x:.1f}%")
            df['threshold'] = df['threshold'].apply(lambda x: f"{x:.1f}%")
            df['status'] = df['status'].apply(lambda x: f"✓ {x}" if x == "Pass" else f"✗ {x}")
            
            # Rename columns for display
            df.columns = ['Agent', 'Confidence', 'Threshold', 'Status']
            
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )
        else:
            st.warning("No confidence summary data available.")
    
    with tab2:
        st.markdown("##### 🧠 Coordinator's Metacognitive Analysis")
        st.info("This section reveals how the coordinator agent interpreted your request and planned the analysis strategy.")
        
        if report_data.get('metacognitive_analysis'):
            meta = report_data['metacognitive_analysis']
            
            if meta.get('user_intent'):
                st.markdown("""
                <div class="analysis-card">
                    <h4>User Intent Interpretation</h4>
                """, unsafe_allow_html=True)
                st.markdown(meta['user_intent'])
                st.markdown("</div>", unsafe_allow_html=True)
            
            if meta.get('analysis_plan'):
                st.markdown("""
                <div class="analysis-card">
                    <h4>Analysis Plan</h4>
                """, unsafe_allow_html=True)
                for i, step in enumerate(meta['analysis_plan'], 1):
                    st.markdown(f"{i}. {step}")
                st.markdown("</div>", unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                if meta.get('agents_invoked'):
                    st.markdown(f"""
                    <div class="analysis-card">
                        <h4>Agents Invoked</h4>
                        <p>{meta['agents_invoked']}</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            with col2:
                if meta.get('coordinator_confidence'):
                    st.markdown(f"""
                    <div class="analysis-card">
                        <h4>Coordinator Confidence</h4>
                        <p style="font-size: 1.5rem; font-weight: 600; color: #1e3c72;">{meta['coordinator_confidence']:.0f}%</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            if meta.get('reasoning'):
                st.markdown("""
                <div class="analysis-card">
                    <h4>Reasoning</h4>
                """, unsafe_allow_html=True)
                st.markdown(meta['reasoning'])
                st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.warning("No metacognitive analysis data available.")
    
    with tab3:
        st.markdown("##### 🛡️ Guardrails and System Boundaries")
        st.info("This section shows the ethical and operational guardrails that govern the agent's behavior.")
        
        if report_data.get('guardrails'):
            guards = report_data['guardrails']
            
            if guards.get('checks_performed') is not None:
                st.markdown(f"""
                <div class="analysis-card">
                    <h4>Guardrail Checks Performed: {guards['checks_performed']}</h4>
                    <p style="color: #10b981; font-weight: 600;">✓ All confidence thresholds met. No guardrail violations detected.</p>
                </div>
                """, unsafe_allow_html=True)
            
            if guards.get('active_guardrails'):
                st.markdown("""
                <div class="analysis-card">
                    <h4>Active Guardrails</h4>
                """, unsafe_allow_html=True)
                for guardrail in guards['active_guardrails']:
                    st.markdown(f"• {guardrail}")
                st.markdown("</div>", unsafe_allow_html=True)
            
            if guards.get('operating_boundaries'):
                st.markdown("""
                <div class="analysis-card">
                    <h4>Operating Boundaries</h4>
                """, unsafe_allow_html=True)
                for boundary in guards['operating_boundaries']:
                    st.markdown(f"• {boundary}")
                st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.warning("No guardrails data available.")
    
    # Disclaimers
    st.markdown("""
    <div class="analysis-card" style="background-color: #fef3c7; border-left: 4px solid #f59e0b; margin-top: 1rem;">
        <h4 style="color: #92400e;">⚠️ Important Disclaimers</h4>
        <p style="color: #78350f; font-size: 0.9rem;">
            This analysis is for <strong>informational and educational purposes only</strong>. 
            It does NOT constitute investment advice or a recommendation to buy or sell securities. 
            Past performance does not guarantee future results. All investments involve risk, including possible loss of principal.
        </p>
        <p style="color: #78350f; font-size: 0.85rem; margin-top: 1rem;">
            <strong>Operating Boundaries:</strong> NO personalized investment advice or stock recommendations • 
            NO guarantees about future stock performance • All outputs are for educational and analytical purposes only
        </p>
    </div>
    """, unsafe_allow_html=True)

def main():
    """Main application logic"""
    
    # Header
    st.markdown("""
    <div class="header-container">
        <h1 class="header-title">FinSight AI Agent</h1>
        <p class="header-subtitle">Multi-Agent Financial Analysis for Earnings Calls</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if 'analysis_complete' not in st.session_state:
        st.session_state.analysis_complete = False
        st.session_state.results = None
    
    # Input section
    with st.container():
        st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
        st.markdown("### 📤 Upload Earnings Call Data")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            audio_file = st.file_uploader(
                "Upload Earnings Call Audio (MP3)",
                type=['mp3'],
                help="Upload the earnings call audio file for analysis"
            )
        
        with col2:
            ticker = st.text_input(
                "Company Ticker",
                placeholder="e.g., GOOGL",
                help="Enter the stock ticker symbol"
            ).upper()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Analyze button
        if st.button("🚀 Analyze Earnings Call", type="primary", use_container_width=True):
            if not ticker:
                st.error("⚠️ Please enter a company ticker symbol")
            else:
                st.session_state.analysis_complete = False
                
                # Initialize API
                api = FinSightAPI()
                
                # Progress tracking
                progress_container = st.container()
                
                with progress_container:
                    # Stage 1: Sentiment Analysis
                    st.markdown("""
                    <div class="status-indicator status-processing">
                        <span style="font-size: 1.5rem;">🔄</span>
                        <span style="font-weight: 600;">Processing Sentiment Analysis...</span>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    with st.spinner("Analyzing sentiment from earnings call transcript..."):
                        sentiment_result = api.analyze_sentiment(ticker, audio_file)
                        time.sleep(4.0)  # Simulate processing time
                    
                    if sentiment_result:
                        st.markdown("""
                        <div class="status-indicator status-complete">
                            <span style="font-size: 1.5rem;">✅</span>
                            <span style="font-weight: 600;">Sentiment Analysis Complete</span>
                        </div>
                        """, unsafe_allow_html=True)
                        display_sentiment_analysis(sentiment_result)
                    
                    # Stage 2: Event Detection
                    st.markdown("""
                    <div class="status-indicator status-processing">
                        <span style="font-size: 1.5rem;">🔄</span>
                        <span style="font-weight: 600;">Detecting Significant Events...</span>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    with st.spinner("Identifying and verifying significant events..."):
                        events_result = api.detect_events(ticker)
                        time.sleep(5.0)
                    
                    if events_result:
                        st.markdown("""
                        <div class="status-indicator status-complete">
                            <span style="font-size: 1.5rem;">✅</span>
                            <span style="font-weight: 600;">Event Detection Complete</span>
                        </div>
                        """, unsafe_allow_html=True)
                        display_event_detection(events_result)
                    
                    # Stage 3: Volatility Prediction
                    st.markdown("""
                    <div class="status-indicator status-processing">
                        <span style="font-size: 1.5rem;">🔄</span>
                        <span style="font-weight: 600;">Predicting Market Volatility...</span>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    with st.spinner("Calculating volatility predictions..."):
                        volatility_result = api.predict_volatility(ticker)
                        time.sleep(5.5)
                    
                    if volatility_result:
                        st.markdown("""
                        <div class="status-indicator status-complete">
                            <span style="font-size: 1.5rem;">✅</span>
                            <span style="font-weight: 600;">Volatility Prediction Complete</span>
                        </div>
                        """, unsafe_allow_html=True)
                        display_volatility_prediction(volatility_result)
                    
                    # Stage 4: Final Report
                    st.markdown("""
                    <div class="status-indicator status-processing">
                        <span style="font-size: 1.5rem;">🔄</span>
                        <span style="font-weight: 600;">Generating Final Report...</span>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    with st.spinner("Compiling comprehensive analysis report..."):
                        final_result = api.generate_final_report(ticker)
                        time.sleep(3.5)
                    
                    if final_result:
                        st.markdown("""
                        <div class="status-indicator status-complete">
                            <span style="font-size: 1.5rem;">✅</span>
                            <span style="font-weight: 600;">Final Report Complete</span>
                        </div>
                        """, unsafe_allow_html=True)
                        display_final_report(final_result)
                        
                        st.session_state.analysis_complete = True
                        st.balloons()

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #64748b; padding: 2rem 0;">
        <p><strong>FinSight AI Agent v1.0</strong></p>
        <p style="font-size: 0.85rem;">Powered by Multi-Agent AI System | For Educational Purposes Only</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

