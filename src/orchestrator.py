"""
Orchestrator - Manages the multi-agent workflow using LangGraph.
"""

import os
from typing import Dict, Any
from datetime import datetime
from langgraph.graph import StateGraph, END, START
from typing_extensions import TypedDict

from .models import (
    FinSightState,
    get_default_self_model,
    DEFAULT_ANALYSIS_QUESTIONS
)
from .agents import (
    CoordinatorAgent,
    SentimentAnalysisAgent,
    EventDetectionAgent,
    VolatilityPredictionAgent
)
from .tools import transcript_reader
from .config import config


class FinSightOrchestrator:
    """Orchestrates the multi-agent financial analysis workflow."""
    
    def __init__(self):
        self.coordinator = CoordinatorAgent()
        self.sentiment_agent = SentimentAnalysisAgent()
        self.event_agent = EventDetectionAgent()
        self.volatility_agent = VolatilityPredictionAgent()
        self.workflow = self._build_workflow()
        self.output_dir = config.paths.output_dir
        os.makedirs(self.output_dir, exist_ok=True)
    
    def _load_transcript_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Load transcript from file."""
        print(f"\n📄 Loading transcript from: {state['transcript_path']}")
        
        content = transcript_reader.read_transcript(state['transcript_path'])
        
        if content.startswith("Error"):
            print(f"❌ {content}")
            return {"transcript_content": "", "errors": [content]}
        
        print(f"✅ Loaded {len(content)} characters")
        return {"transcript_content": content}
    
    def _coordinator_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Coordinator planning node."""
        print("\n🧠 COORDINATOR: Planning analysis...")
        result = self.coordinator.process(state)
        return result
    
    def _sentiment_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Sentiment analysis node."""
        print("\n😊 SENTIMENT AGENT: Analyzing sentiment...")
        result = self.sentiment_agent.process(state)
        
        # Save individual agent report
        if result.get('sentiment_result'):
            self._save_agent_report(
                state['company_ticker'],
                'sentiment',
                result['sentiment_result']
            )
        
        return result
    
    def _event_detection_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Event detection node."""
        print("\n🔍 EVENT DETECTION AGENT: Detecting significant events...")
        result = self.event_agent.process(state)
        
        # Save individual agent report
        if result.get('event_detection_result'):
            self._save_agent_report(
                state['company_ticker'],
                'event_detection',
                result['event_detection_result']
            )
        
        return result
    
    def _volatility_prediction_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Volatility prediction node."""
        print("\n📊 VOLATILITY AGENT: Predicting volatility...")
        result = self.volatility_agent.process(state)
        
        # Save individual agent report
        if result.get('volatility_result'):
            self._save_agent_report(
                state['company_ticker'],
                'volatility',
                result['volatility_result']
            )
        
        return result
    
    def _synthesize_report_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Create final comprehensive report."""
        print("\n📝 SYNTHESIZING: Generating final report...")
        
        sent = state.get('sentiment_result')
        events = state.get('event_detection_result')
        vol = state.get('volatility_result')
        decision = state.get('metacognitive_decision')
        
        # Generate comprehensive report
        report = self._generate_final_report(state, sent, events, vol, decision)
        
        print("✅ Final report generated")
        return {"final_report": report}
    
    def _generate_final_report(self, state, sent, events, vol, decision) -> str:
        """Generate the final markdown report."""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ticker = state['company_ticker']
        
        # Executive summary values
        sentiment_name = sent.overall_sentiment if sent else 'N/A'
        sentiment_score = f"{sent.sentiment_score:.2f}" if sent else "0.00"
        sentiment_conf = f"{sent.confidence:.2%}" if sent else "0%"
        
        events_total = events.total_events_found if events else 0
        events_verified = events.verified_count if events else 0
        events_conf = f"{events.confidence:.2%}" if events else "0%"
        
        volatility_name = vol.predicted_volatility if vol else 'N/A'
        volatility_score = f"{vol.volatility_score:.2f}" if vol else "0.00"
        volatility_conf = f"{vol.confidence:.2%}" if vol else "0%"
        hist_vol = f"{vol.historical_volatility:.2%}" if vol else "0%"
        
        # Build report
        report = f"""# FinSight Multi-Agent Analysis Report

**Generated:** {timestamp}  
**Company:** {ticker}  
**System Version:** {state['self_model'].version}

---

## Executive Summary

- **Sentiment:** {sentiment_name} (Score: {sentiment_score}, Confidence: {sentiment_conf})
- **Events Detected:** {events_total} ({events_verified} verified, Confidence: {events_conf})
- **Predicted Volatility:** {volatility_name} (Score: {volatility_score}, Confidence: {volatility_conf})
- **Historical Volatility:** {hist_vol}

---

## 1. Coordinator's Metacognitive Analysis

"""
        
        if decision:
            report += f"""**User Intent:** {decision.user_intent}

**Analysis Plan:**
"""
            for i, step in enumerate(decision.analysis_plan, 1):
                # Strip any leading numbers and dots/spaces from LLM output
                clean_step = step.lstrip('0123456789. ')
                report += f"{i}. {clean_step}\n"
            
            report += f"\n**Agents Invoked:** {', '.join(decision.agents_to_invoke)}\n"
            report += f"**Coordinator Confidence:** {decision.confidence:.2%}\n"
            report += f"\n**Reasoning:** {decision.reasoning}\n"
        
        report += "\n---\n\n## 2. Sentiment Analysis\n\n"
        
        if sent:
            report += f"""**Overall Sentiment:** {sent.overall_sentiment}  
**Sentiment Score:** {sent.sentiment_score:.2f} (range: -1.0 to 1.0)  
**Confidence:** {sent.confidence:.2%}

**Market Sentiment Summary:**
{sent.market_sentiment}

**Key Sentiment Drivers:**
"""
            for driver in sent.key_sentiment_drivers:
                report += f"- {driver}\n"
            
            if sent.news_headlines:
                report += "\n**News Headlines Analyzed:**\n"
                for headline in sent.news_headlines:
                    report += f"- {headline}\n"
            
            if sent.tool_validations:
                report += "\n**Tool Validations:**\n"
                for validation in sent.tool_validations:
                    report += f"- {validation}\n"
        else:
            report += "*Sentiment analysis not available.*\n"
        
        report += "\n---\n\n## 3. Significant Event Detection\n\n"
        
        if events:
            report += f"""**Total Events Found:** {events.total_events_found}  
**Verified Events:** {events.verified_count}  
**Confidence:** {events.confidence:.2%}

**Detected Events:**
"""
            for i, event in enumerate(events.events, 1):
                report += f"""
### Event {i}: {event.event_type}

- **Description:** {event.description}
- **Mentioned in Call:** {'Yes' if event.mentioned_in_call else 'No'}
- **Verified:** {'Yes' if event.verified else 'No'}
- **Source:** {event.source}
- **Impact Assessment:** {event.impact_assessment.upper()}
"""
            
            if events.tool_validations:
                report += "\n**Tool Validations:**\n"
                for validation in events.tool_validations:
                    report += f"- {validation}\n"
        else:
            report += "*Event detection not available.*\n"
        
        report += "\n---\n\n## 4. Volatility Prediction\n\n"
        
        if vol:
            report += f"""**Predicted Volatility:** {vol.predicted_volatility}  
**Volatility Score:** {vol.volatility_score:.2f} (range: 0.0 to 1.0)  
**Historical Volatility:** {vol.historical_volatility:.2%}  
**Confidence:** {vol.confidence:.2%}

**Key Volatility Drivers:**
"""
            for driver in vol.key_volatility_drivers:
                report += f"- {driver}\n"
            
            report += f"\n**Sentiment Impact:**\n{vol.sentiment_impact}\n"
            report += f"\n**Event Impact:**\n{vol.event_impact}\n"
            
            if vol.tool_validations:
                report += "\n**Tool Validations:**\n"
                for validation in vol.tool_validations:
                    report += f"- {validation}\n"
            
            if vol.transcript_insights:
                report += "\n### Transcript Insights\n\n"
                for insight in vol.transcript_insights:
                    report += f"""#### {insight.focus_item}
**Question:** {insight.question}  
**Answer:** {insight.answer}  
**Confidence:** {insight.confidence:.2%}

"""
        else:
            report += "*Volatility prediction not available.*\n"
        
        report += "\n---\n\n## 5. Guardrails and System Boundaries\n\n"
        
        guardrails = state.get('guardrails_applied', [])
        report += f"**Guardrail Checks Performed:** {len(guardrails)}\n\n"
        
        if guardrails:
            for g in guardrails:
                report += f"""- **{g.guardrail_type}** ({g.agent})
  - {g.description}
  - Action: {g.action_taken}
"""
        else:
            report += "*All confidence thresholds met. No guardrail violations detected.*\n"
        
        report += "\n**Active Guardrails:**\n"
        for guardrail in state['self_model'].active_guardrails:
            report += f"- {guardrail}\n"
        
        report += "\n**Operating Boundaries:**\n"
        for boundary in state['self_model'].operating_boundaries:
            report += f"- {boundary}\n"
        
        report += "\n---\n\n## 6. System Confidence Summary\n\n"
        
        self_model = state['self_model']
        report += "| Agent | Confidence | Threshold | Status |\n"
        report += "|-------|-----------|-----------|--------|\n"
        
        if sent:
            threshold = self_model.agent_capabilities[0].confidence_threshold
            status = "✓ Pass" if sent.confidence >= threshold else "⚠ Low"
            report += f"| Sentiment Analysis | {sent.confidence:.2%} | {threshold:.2%} | {status} |\n"
        
        if events:
            threshold = self_model.agent_capabilities[1].confidence_threshold
            status = "✓ Pass" if events.confidence >= threshold else "⚠ Low"
            report += f"| Event Detection | {events.confidence:.2%} | {threshold:.2%} | {status} |\n"
        
        if vol:
            threshold = self_model.agent_capabilities[2].confidence_threshold
            status = "✓ Pass" if vol.confidence >= threshold else "⚠ Low"
            report += f"| Volatility Prediction | {vol.confidence:.2%} | {threshold:.2%} | {status} |\n"
        
        report += "\n---\n\n## Disclaimers\n\n"
        report += f"**Mission:** {self_model.mission}\n\n"
        report += "This analysis is for **informational and educational purposes only**. "
        report += "It does NOT constitute investment advice or a recommendation to buy or sell securities. "
        report += "Past performance does not guarantee future results. "
        report += "All investments involve risk, including possible loss of principal.\n\n"
        report += f"**Generated by:** {self_model.system_name} v{self_model.version}\n"
        
        return report
    
    def _save_agent_report(self, ticker: str, agent_name: str, result: Any):
        """Save individual agent report to markdown file."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{agent_name}_{ticker}_{timestamp}.md"
        filepath = os.path.join(self.output_dir, filename)
        
        report = self._format_agent_report(agent_name, ticker, result)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"  💾 Saved {agent_name} report: {filename}")
    
    def _format_agent_report(self, agent_name: str, ticker: str, result: Any) -> str:
        """Format individual agent result as markdown."""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        if agent_name == 'sentiment':
            return f"""# Sentiment Analysis Report

**Ticker:** {ticker}  
**Generated:** {timestamp}  
**Agent:** Sentiment Analysis Agent

---

## Overall Assessment

- **Sentiment:** {result.overall_sentiment}
- **Score:** {result.sentiment_score:.2f} (range: -1.0 to 1.0)
- **Confidence:** {result.confidence:.2%}

## Market Sentiment

{result.market_sentiment}

## Key Sentiment Drivers

{chr(10).join(f'- {driver}' for driver in result.key_sentiment_drivers)}

## News Headlines Analyzed

{chr(10).join(f'- {headline}' for headline in result.news_headlines) if result.news_headlines else 'None'}

## Tool Validations

{chr(10).join(f'- {v}' for v in result.tool_validations) if result.tool_validations else 'None'}
"""
        
        elif agent_name == 'event_detection':
            events_section = ""
            for i, event in enumerate(result.events, 1):
                events_section += f"""
### Event {i}: {event.event_type}

- **Description:** {event.description}
- **Mentioned in Call:** {'Yes' if event.mentioned_in_call else 'No'}
- **Verified:** {'Yes' if event.verified else 'No'}
- **Source:** {event.source}
- **Impact:** {event.impact_assessment.upper()}
"""
            
            return f"""# Event Detection Report

**Ticker:** {ticker}  
**Generated:** {timestamp}  
**Agent:** Significant Event Detection Agent

---

## Summary

- **Total Events Found:** {result.total_events_found}
- **Verified Events:** {result.verified_count}
- **Confidence:** {result.confidence:.2%}

## Detected Events

{events_section if events_section else '*No events detected*'}

## Tool Validations

{chr(10).join(f'- {v}' for v in result.tool_validations) if result.tool_validations else 'None'}
"""
        
        elif agent_name == 'volatility':
            insights_section = ""
            for insight in result.transcript_insights:
                insights_section += f"""
### {insight.focus_item}

**Question:** {insight.question}  
**Answer:** {insight.answer}  
**Confidence:** {insight.confidence:.2%}
"""
            
            return f"""# Volatility Prediction Report

**Ticker:** {ticker}  
**Generated:** {timestamp}  
**Agent:** Volatility Prediction Agent

---

## Prediction

- **Predicted Volatility:** {result.predicted_volatility}
- **Volatility Score:** {result.volatility_score:.2f} (range: 0.0 to 1.0)
- **Historical Volatility:** {result.historical_volatility:.2%}
- **Confidence:** {result.confidence:.2%}

## Key Volatility Drivers

{chr(10).join(f'- {driver}' for driver in result.key_volatility_drivers)}

## Sentiment Impact

{result.sentiment_impact}

## Event Impact

{result.event_impact}

## Transcript Insights

{insights_section if insights_section else '*No insights available*'}

## Tool Validations

{chr(10).join(f'- {v}' for v in result.tool_validations) if result.tool_validations else 'None'}
"""
        
        return f"# {agent_name.title()} Report\n\n*Report format not implemented*"
    
    def _build_workflow(self) -> StateGraph:
        """Build the LangGraph workflow."""
        # Define TypedDict for LangGraph state
        class GraphState(TypedDict):
            user_query: str
            company_ticker: str
            transcript_path: str
            analysis_questions: list
            self_model: Any
            metacognitive_decision: Any
            transcript_content: str
            sentiment_result: Any
            event_detection_result: Any
            volatility_result: Any
            final_report: str
            guardrails_applied: list
            errors: list
        
        # Create workflow
        workflow = StateGraph(GraphState)
        
        # Add nodes
        workflow.add_node("coordinator", self._coordinator_node)
        workflow.add_node("load_transcript", self._load_transcript_node)
        workflow.add_node("sentiment_analysis", self._sentiment_node)
        workflow.add_node("event_detection", self._event_detection_node)
        workflow.add_node("volatility_prediction", self._volatility_prediction_node)
        workflow.add_node("synthesize_report", self._synthesize_report_node)
        
        # Define workflow edges
        workflow.set_entry_point("coordinator")
        workflow.add_edge("coordinator", "load_transcript")
        workflow.add_edge("load_transcript", "sentiment_analysis")
        workflow.add_edge("sentiment_analysis", "event_detection")
        workflow.add_edge("event_detection", "volatility_prediction")
        workflow.add_edge("volatility_prediction", "synthesize_report")
        workflow.add_edge("synthesize_report", END)
        
        return workflow.compile()
    
    def run_analysis(self, transcript_path: str, ticker: str, user_query: str = None) -> Dict[str, Any]:
        """Run the complete multi-agent analysis."""
        print("\n" + "="*80)
        print("🚀 FinSight Multi-Agent Analysis System")
        print("="*80)
        print(f"\n📊 Ticker: {ticker}")
        print(f"📄 Transcript: {transcript_path}")
        
        if user_query is None:
            user_query = (
                f"Provide a comprehensive analysis of {ticker}'s earnings call, "
                "including sentiment, significant events, and volatility prediction."
            )
        
        print(f"❓ Query: {user_query}\n")
        
        # Initialize state
        initial_state = {
            "user_query": user_query,
            "company_ticker": ticker,
            "transcript_path": transcript_path,
            "analysis_questions": DEFAULT_ANALYSIS_QUESTIONS,
            "self_model": get_default_self_model(),
            "guardrails_applied": [],
            "errors": []
        }
        
        try:
            # Run workflow
            result = self.workflow.invoke(initial_state)
            
            # Save final report
            if result.get('final_report'):
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"final_report_{ticker}_{timestamp}.md"
                filepath = os.path.join(self.output_dir, filename)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(result['final_report'])
                
                print(f"\n✅ Final report saved: {filepath}")
            
            # Check for errors
            if result.get('errors'):
                print("\n⚠️  Errors encountered:")
                for error in result['errors']:
                    print(f"  - {error}")
            
            print("\n" + "="*80)
            print("✅ Analysis Complete!")
            print("="*80 + "\n")
            
            return result
        
        except Exception as e:
            print(f"\n❌ Error during analysis: {str(e)}")
            raise

