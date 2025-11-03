"""
FinSight API Stub
Simulates backend processing by returning pre-generated analysis files
"""

import re
from pathlib import Path
from typing import Dict, Optional, Any
from datetime import datetime

class FinSightAPI:
    """
    Stubbed API for FinSight AI Agent
    
    This implementation simulates the backend processing by:
    1. Pretending to accept MP3 audio files
    2. Using existing transcript in txt format
    3. Returning pre-generated markdown analysis files
    """
    
    def __init__(self):
        self.data_dir = Path(__file__).parent / "data"
        self.input_dir = self.data_dir / "input"
        self.output_dir = self.data_dir / "output"
        
    def _parse_markdown_file(self, file_path: Path) -> Dict[str, Any]:
        """Parse markdown file and extract structured data"""
        if not file_path.exists():
            return {}
        
        content = file_path.read_text()
        return {"raw_content": content, "parsed": self._extract_metadata(content)}
    
    def _extract_metadata(self, content: str) -> Dict[str, Any]:
        """Extract metadata from markdown content"""
        metadata = {}
        
        # Extract key-value pairs from markdown
        patterns = {
            'ticker': r'\*\*Ticker:\*\*\s*(\w+)',
            'generated': r'\*\*Generated:\*\*\s*([^\n]+)',
            'agent': r'\*\*Agent:\*\*\s*([^\n]+)',
            'sentiment': r'\*\*Sentiment:\*\*\s*(\w+)',
            'score': r'\*\*Score:\*\*\s*([-\d.]+)',
            'confidence': r'\*\*Confidence:\*\*\s*([\d.]+)%',
            'total_events': r'\*\*Total Events Found:\*\*\s*(\d+)',
            'verified_events': r'\*\*Verified Events:\*\*\s*(\d+)',
            'predicted_volatility': r'\*\*Predicted Volatility:\*\*\s*(\w+)',
            'volatility_score': r'\*\*Volatility Score:\*\*\s*([\d.]+)',
            'historical_volatility': r'\*\*Historical Volatility:\*\*\s*([\d.]+)%',
        }
        
        for key, pattern in patterns.items():
            match = re.search(pattern, content)
            if match:
                value = match.group(1)
                # Convert to appropriate type
                if key in ['score', 'volatility_score', 'historical_volatility']:
                    metadata[key] = float(value)
                elif key in ['total_events', 'verified_events']:
                    metadata[key] = int(value)
                elif key == 'confidence':
                    metadata[key] = float(value)
                else:
                    metadata[key] = value
        
        return metadata
    
    def analyze_sentiment(self, ticker: str, audio_file=None) -> Dict[str, Any]:
        """
        Analyze sentiment from earnings call
        
        Args:
            ticker: Stock ticker symbol
            audio_file: MP3 audio file (currently ignored in stub)
            
        Returns:
            Dictionary containing sentiment analysis results
        """
        # In stub mode, find the latest sentiment file for the ticker
        sentiment_files = list(self.output_dir.glob(f"sentiment_{ticker}_*.md"))
        
        if not sentiment_files:
            return None
        
        # Get the most recent file
        latest_file = max(sentiment_files, key=lambda p: p.stat().st_mtime)
        content = latest_file.read_text()
        
        # Parse the markdown content
        metadata = self._extract_metadata(content)
        
        # Extract market sentiment summary
        market_summary = ""
        summary_match = re.search(r'## Market Sentiment\n\n(.*?)\n\n##', content, re.DOTALL)
        if summary_match:
            market_summary = summary_match.group(1).strip()
        
        # Extract key drivers
        key_drivers = []
        drivers_match = re.search(r'## Key Sentiment Drivers\n\n(.*?)\n\n##', content, re.DOTALL)
        if drivers_match:
            driver_text = drivers_match.group(1).strip()
            key_drivers = [line.strip('- ').strip() for line in driver_text.split('\n') if line.strip().startswith('-')]
        
        # Extract tool validations
        tool_validations = []
        validations_match = re.search(r'\*\*Tool Validations:\*\*\n(.*?)(?:\n\n##|\n\n---|\Z)', content, re.DOTALL)
        if validations_match:
            validation_text = validations_match.group(1).strip()
            tool_validations = [line.strip('- ').strip() for line in validation_text.split('\n') if line.strip().startswith('-')]
        
        # Extract news headlines
        news_headlines = []
        headlines_match = re.search(r'\*\*News Headlines Analyzed:\*\*\n(.*?)(?:\n\n\*\*|\n\n##|\Z)', content, re.DOTALL)
        if headlines_match:
            headlines_text = headlines_match.group(1).strip()
            news_headlines = [line.strip('- ').strip() for line in headlines_text.split('\n') if line.strip().startswith('-')]
        
        return {
            'ticker': metadata.get('ticker', ticker),
            'sentiment': metadata.get('sentiment', 'positive'),
            'score': metadata.get('score', 0.75),
            'confidence': metadata.get('confidence', 85.0),
            'market_summary': market_summary,
            'key_drivers': key_drivers,
            'tool_validations': tool_validations,
            'news_headlines': news_headlines,
            'generated': metadata.get('generated', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        }
    
    def detect_events(self, ticker: str) -> Dict[str, Any]:
        """
        Detect significant events from earnings call
        
        Args:
            ticker: Stock ticker symbol
            
        Returns:
            Dictionary containing detected events
        """
        # Find the latest event detection file
        event_files = list(self.output_dir.glob(f"event_detection_{ticker}_*.md"))
        
        if not event_files:
            return None
        
        latest_file = max(event_files, key=lambda p: p.stat().st_mtime)
        content = latest_file.read_text()
        
        # Parse metadata
        metadata = self._extract_metadata(content)
        
        # Extract individual events
        events = []
        event_sections = re.findall(
            r'### Event \d+: (\w+)\n\n(.*?)\n\n(?:###|\n##|\Z)',
            content,
            re.DOTALL
        )
        
        for event_type, event_content in event_sections:
            # Extract event details
            description_match = re.search(r'\*\*Description:\*\*\s*(.*?)\n', event_content)
            impact_match = re.search(r'\*\*Impact:\*\*\s*(\w+)', event_content)
            source_match = re.search(r'\*\*Source:\*\*\s*(\w+)', event_content)
            verified_match = re.search(r'\*\*Verified:\*\*\s*(\w+)', event_content)
            
            event = {
                'type': event_type,
                'description': description_match.group(1) if description_match else '',
                'impact': impact_match.group(1) if impact_match else 'MEDIUM',
                'source': source_match.group(1) if source_match else 'transcript',
                'verified': verified_match.group(1).lower() == 'yes' if verified_match else True
            }
            events.append(event)
        
        # Extract tool validations
        tool_validations = []
        validations_match = re.search(r'\*\*Tool Validations:\*\*\n(.*?)(?:\n\n##|\n\n---|\Z)', content, re.DOTALL)
        if validations_match:
            validation_text = validations_match.group(1).strip()
            tool_validations = [line.strip('- ').strip() for line in validation_text.split('\n') if line.strip().startswith('-')]
        
        return {
            'ticker': ticker,
            'total_events': metadata.get('total_events', len(events)),
            'verified_events': metadata.get('verified_events', len(events)),
            'confidence': metadata.get('confidence', 90.0),
            'events': events,
            'tool_validations': tool_validations,
            'generated': metadata.get('generated', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        }
    
    def predict_volatility(self, ticker: str) -> Dict[str, Any]:
        """
        Predict market volatility based on earnings call
        
        Args:
            ticker: Stock ticker symbol
            
        Returns:
            Dictionary containing volatility predictions
        """
        # Find the latest volatility file
        volatility_files = list(self.output_dir.glob(f"volatility_{ticker}_*.md"))
        
        if not volatility_files:
            return None
        
        latest_file = max(volatility_files, key=lambda p: p.stat().st_mtime)
        content = latest_file.read_text()
        
        # Parse metadata
        metadata = self._extract_metadata(content)
        
        # Extract key drivers
        key_drivers = []
        drivers_match = re.search(r'## Key Volatility Drivers\n\n(.*?)\n\n##', content, re.DOTALL)
        if drivers_match:
            driver_text = drivers_match.group(1).strip()
            key_drivers = [line.strip('- ').strip() for line in driver_text.split('\n') if line.strip().startswith('-')]
        
        # Extract sentiment impact
        sentiment_impact = ""
        sentiment_match = re.search(r'## Sentiment Impact\n\n(.*?)\n\n##', content, re.DOTALL)
        if sentiment_match:
            sentiment_impact = sentiment_match.group(1).strip()
        
        # Extract event impact
        event_impact = ""
        event_match = re.search(r'## Event Impact\n\n(.*?)\n\n##', content, re.DOTALL)
        if event_match:
            event_impact = event_match.group(1).strip()
        
        # Extract tool validations
        tool_validations = []
        validations_match = re.search(r'\*\*Tool Validations:\*\*\n(.*?)(?:\n\n###|\n\n##|\Z)', content, re.DOTALL)
        if validations_match:
            validation_text = validations_match.group(1).strip()
            tool_validations = [line.strip('- ').strip() for line in validation_text.split('\n') if line.strip().startswith('-')]
        
        # Extract transcript insights
        transcript_insights = []
        insights_section = re.search(r'### Transcript Insights\n\n(.*?)(?:\n\n##|\n\n---|\Z)', content, re.DOTALL)
        if insights_section:
            insights_text = insights_section.group(1).strip()
            # Parse individual insights
            insight_blocks = re.findall(
                r'#### (.*?)\n\*\*Question:\*\*\s*(.*?)\n\*\*Answer:\*\*\s*(.*?)\n\*\*Confidence:\*\*\s*([\d.]+)%',
                insights_text,
                re.DOTALL
            )
            for title, question, answer, confidence in insight_blocks:
                transcript_insights.append({
                    'title': title.strip(),
                    'question': question.strip(),
                    'answer': answer.strip(),
                    'confidence': float(confidence)
                })
        
        return {
            'ticker': ticker,
            'predicted_volatility': metadata.get('predicted_volatility', 'medium'),
            'volatility_score': metadata.get('volatility_score', 0.65),
            'historical_volatility': metadata.get('historical_volatility', 20.0),
            'confidence': metadata.get('confidence', 85.0),
            'key_drivers': key_drivers,
            'sentiment_impact': sentiment_impact,
            'event_impact': event_impact,
            'tool_validations': tool_validations,
            'transcript_insights': transcript_insights,
            'generated': metadata.get('generated', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        }
    
    def generate_final_report(self, ticker: str) -> Dict[str, Any]:
        """
        Generate comprehensive final report
        
        Args:
            ticker: Stock ticker symbol
            
        Returns:
            Dictionary containing comprehensive analysis
        """
        # Find the latest final report file
        report_files = list(self.output_dir.glob(f"final_report_{ticker}_*.md"))
        
        if not report_files:
            return None
        
        latest_file = max(report_files, key=lambda p: p.stat().st_mtime)
        content = latest_file.read_text()
        
        # Extract executive summary data
        summary_section = re.search(
            r'## Executive Summary\n\n(.*?)\n\n---',
            content,
            re.DOTALL
        )
        
        # Parse summary for key metrics
        sentiment_match = re.search(r'\*\*Sentiment:\*\*\s*(\w+)\s*\(Score:\s*([\d.]+),\s*Confidence:\s*([\d.]+)%\)', content)
        events_match = re.search(r'\*\*Events Detected:\*\*\s*(\d+)\s*\((\d+)\s*verified,\s*Confidence:\s*([\d.]+)%\)', content)
        volatility_match = re.search(r'\*\*Predicted Volatility:\*\*\s*(\w+)\s*\(Score:\s*([\d.]+),\s*Confidence:\s*([\d.]+)%\)', content)
        hist_vol_match = re.search(r'\*\*Historical Volatility:\*\*\s*([\d.]+)%', content)
        
        # Extract coordinator's metacognitive analysis
        metacognitive = {}
        meta_section = re.search(
            r'## 1\. Coordinator\'s Metacognitive Analysis\n\n(.*?)(?:\n\n---|\n\n##)',
            content,
            re.DOTALL
        )
        if meta_section:
            meta_text = meta_section.group(1).strip()
            # Extract specific fields
            user_intent_match = re.search(r'\*\*User Intent:\*\*\s*(.*?)(?:\n\n\*\*|\Z)', meta_text, re.DOTALL)
            plan_match = re.search(r'\*\*Analysis Plan:\*\*\s*(.*?)(?:\n\n\*\*|\Z)', meta_text, re.DOTALL)
            agents_match = re.search(r'\*\*Agents Invoked:\*\*\s*(.*?)(?:\n|\Z)', meta_text)
            coord_conf_match = re.search(r'\*\*Coordinator Confidence:\*\*\s*([\d.]+)%', meta_text)
            reasoning_match = re.search(r'\*\*Reasoning:\*\*\s*(.*?)(?:\n\n---|\Z)', meta_text, re.DOTALL)
            
            if user_intent_match:
                metacognitive['user_intent'] = user_intent_match.group(1).strip()
            if plan_match:
                plan_text = plan_match.group(1).strip()
                # Extract numbered list
                plan_items = re.findall(r'\d+\.\s*(.*?)(?=\n\d+\.|\Z)', plan_text, re.DOTALL)
                metacognitive['analysis_plan'] = [item.strip() for item in plan_items]
            if agents_match:
                metacognitive['agents_invoked'] = agents_match.group(1).strip()
            if coord_conf_match:
                metacognitive['coordinator_confidence'] = float(coord_conf_match.group(1))
            if reasoning_match:
                metacognitive['reasoning'] = reasoning_match.group(1).strip()
        
        # Extract confidence summary table
        confidence_summary = []
        table_match = re.search(r'\|\s*Agent\s*\|\s*Confidence.*?\n\|.*?\n((?:\|.*?\n)+)', content)
        if table_match:
            rows = table_match.group(1).strip().split('\n')
            for row in rows:
                cols = [col.strip() for col in row.split('|')[1:-1]]
                if len(cols) >= 4:
                    agent_name = cols[0]
                    conf = float(cols[1].replace('%', ''))
                    thresh = float(cols[2].replace('%', ''))
                    status = 'Pass' if '✓' in cols[3] else 'Fail'
                    
                    confidence_summary.append({
                        'agent': agent_name,
                        'confidence': conf,
                        'threshold': thresh,
                        'status': status
                    })
        
        # Extract guardrails section
        guardrails = {}
        guardrails_section = re.search(
            r'## 5\. Guardrails and System Boundaries\n\n(.*?)(?:\n\n---|\n\n##)',
            content,
            re.DOTALL
        )
        if guardrails_section:
            guard_text = guardrails_section.group(1).strip()
            checks_match = re.search(r'\*\*Guardrail Checks Performed:\*\*\s*(\d+)', guard_text)
            if checks_match:
                guardrails['checks_performed'] = int(checks_match.group(1))
            
            # Extract active guardrails
            active_guards = []
            active_match = re.search(r'\*\*Active Guardrails:\*\*\n(.*?)(?:\n\n\*\*|\Z)', guard_text, re.DOTALL)
            if active_match:
                active_text = active_match.group(1).strip()
                active_guards = [line.strip('- ').strip() for line in active_text.split('\n') if line.strip().startswith('-')]
            guardrails['active_guardrails'] = active_guards
            
            # Extract operating boundaries
            boundaries = []
            boundaries_match = re.search(r'\*\*Operating Boundaries:\*\*\n(.*?)(?:\n\n---|\Z)', guard_text, re.DOTALL)
            if boundaries_match:
                boundaries_text = boundaries_match.group(1).strip()
                boundaries = [line.strip('- ').strip() for line in boundaries_text.split('\n') if line.strip().startswith('-')]
            guardrails['operating_boundaries'] = boundaries
        
        # Extract generation timestamp
        gen_match = re.search(r'\*\*Generated:\*\*\s*([^\n]+)', content)
        version_match = re.search(r'\*\*System Version:\*\*\s*([^\n]+)', content)
        
        return {
            'ticker': ticker,
            'generated': gen_match.group(1) if gen_match else datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'version': version_match.group(1) if version_match else '1.0',
            'sentiment': sentiment_match.group(1) if sentiment_match else 'positive',
            'sentiment_score': float(sentiment_match.group(2)) if sentiment_match else 0.75,
            'sentiment_confidence': float(sentiment_match.group(3)) if sentiment_match else 85.0,
            'events_detected': int(events_match.group(1)) if events_match else 0,
            'events_verified': int(events_match.group(2)) if events_match else 0,
            'events_confidence': float(events_match.group(3)) if events_match else 85.0,
            'predicted_volatility': volatility_match.group(1) if volatility_match else 'medium',
            'volatility_score': float(volatility_match.group(2)) if volatility_match else 0.65,
            'volatility_confidence': float(volatility_match.group(3)) if volatility_match else 85.0,
            'historical_volatility': float(hist_vol_match.group(1)) if hist_vol_match else 20.0,
            'confidence_summary': confidence_summary,
            'metacognitive_analysis': metacognitive,
            'guardrails': guardrails
        }
    
    def process_earnings_call(self, ticker: str, audio_file=None) -> Dict[str, Any]:
        """
        Process complete earnings call analysis (all stages)
        
        Args:
            ticker: Stock ticker symbol
            audio_file: MP3 audio file (currently ignored in stub)
            
        Returns:
            Dictionary containing all analysis results
        """
        return {
            'sentiment': self.analyze_sentiment(ticker, audio_file),
            'events': self.detect_events(ticker),
            'volatility': self.predict_volatility(ticker),
            'final_report': self.generate_final_report(ticker)
        }

