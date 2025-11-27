![badge-labs](https://user-images.githubusercontent.com/327285/230928932-7c75f8ed-e57b-41db-9fb7-a292a13a1e58.svg)

# FinSight Agent: Metacognitive Multi-Agent Financial Analysis System

An advanced multi-agent system that performs comprehensive financial analysis of earnings calls using metacognitive reasoning and specialized expert agents.

---

## 📑 Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Architecture](#architecture)
- [Metacognitive Self-Model & LLM-as-Judge](#metacognitive-self-model--llm-as-judge)
- [Output Reports](#output-reports)
- [Project Structure](#project-structure)
- [Agent Details](#agent-details)
- [Tool Integration](#tool-integration)
- [Guardrails & Safety](#guardrails--safety)
- [Configuration & Customization](#configuration--customization)
- [Troubleshooting](#troubleshooting)
- [Development](#development)
- [Examples](#examples)
- [Dependencies](#dependencies)
- [License](#license)

---

## Overview

FinSight Agent is a production-ready multi-agent system that analyzes earnings call transcripts using **metacognitive self-awareness** and **LLM-as-Judge** patterns for runtime quality control:

- **Metacognitive Self-Model**: System maintains awareness of its own capabilities, limitations, and confidence thresholds
- **LLM-as-Judge**: Each agent self-scores confidence in findings; automated guardrail enforcement at runtime
- **4 Specialized Agents**: Coordinator, Sentiment Analysis, Event Detection, and Volatility Prediction
- **External Tool Validation**: Tavily news search, SEC EDGAR filings, and yfinance market data
- **Confidence-Based Guardrails**: Automated quality control with 60-70% minimum confidence thresholds
- **Individual Reports**: Separate markdown outputs for each agent plus comprehensive final report with transparency
- **Transparent Uncertainty**: All outputs include confidence scores, limitations, and guardrail check results

### Key Features

✅ **Metacognitive Self-Model** - System maintains self-awareness of capabilities, limitations, and boundaries  
✅ **LLM-as-Judge Integration** - Each agent self-scores confidence; runtime guardrail enforcement  
✅ **Multi-Agent Orchestration** - LangGraph-based workflow with metacognitive coordinator  
✅ **Tool-Enhanced Validation** - Each agent uses external APIs to verify findings  
✅ **Confidence Threshold Guardrails** - Automated quality control with 65-70% minimum thresholds  
✅ **Transparent Uncertainty** - All outputs include confidence levels and limitations  
✅ **Structured Outputs** - Pydantic models ensure type safety and validation  
✅ **Individual Reports** - 4 separate markdown reports per analysis  
✅ **Configurable** - Customizable questions, thresholds, and model parameters  
✅ **Production-Ready** - Proper error handling, logging, and CLI interface

---

## Quick Start

### 1. Install
```bash
cd /Users/vincent/Code/finsight-agent
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure
```bash
cp .env.example .env
# Edit .env with your API keys:
# - SCW_DEFAULT_PROJECT_ID
# - SCW_SECRET_KEY
# - TAVILY_API_KEY
```

### 3. Test Setup
```bash
python test_setup.py
```

### 4. Run Analysis
```bash
python -m src.main \
  --transcript data/input/Alphabet_2025_Q1_Earnings_Call_complete_transcript.txt \
  --ticker GOOGL
```

### 5. View Reports
```bash
ls -l data/output/
```

---

## Installation

### Prerequisites

- **Python 3.11+**
- **Internet connection** (for API calls)
- **~500 MB disk space**

### Setup Steps

1. **Navigate to project directory:**
   ```bash
   cd /Users/vincent/Code/finsight-agent
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # macOS/Linux
   # OR
   .venv\Scripts\activate     # Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   
   Or using UV (recommended):
   ```bash
   uv pip install -e .
   ```

4. **Verify installation:**
   ```bash
   python test_setup.py
   ```

---

## Configuration

### Required Environment Variables

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Add your API keys:

```bash
# Scaleway GenAI API
SCW_DEFAULT_PROJECT_ID=your_scaleway_project_id_here
SCW_SECRET_KEY=your_scaleway_secret_key_here

# Tavily Search API
TAVILY_API_KEY=your_tavily_api_key_here
```

### Getting API Keys

**Scaleway GenAI:**
1. Go to https://console.scaleway.com/
2. Navigate to AI/ML → Generative APIs
3. Create project and get credentials

**Tavily Search:**
1. Go to https://tavily.com/
2. Sign up and get API key

### Model Configuration

The system uses Scaleway GenAI with these default parameters:

```python
Model: qwen3-235b-a22b-instruct-2507
Temperature: 0.0 (deterministic)
Max Tokens: 2048
```

To modify, edit `src/config.py`:

```python
@dataclass
class ScalewayConfig:
    model: str = "qwen3-235b-a22b-instruct-2507"
    temperature: float = 0.0
    max_tokens: int = 2048
```

---

## Usage

### Web Interface (Streamlit)

**Launch the interactive web application:**
```bash
streamlit run app.py
```

The Streamlit interface provides a professional dashboard that displays:
- Sentiment analysis with confidence metrics and news validation
- Event detection with SEC filing verification
- Volatility predictions with market data
- Comprehensive final report with metacognitive analysis and guardrails
- Tabbed interface separating analysis outputs from audit/validation data

**Note:** Currently uses a stubbed API that reads pre-generated reports from `data/output/` for demonstration. To integrate with live backend, replace API stubs in `api.py` with calls to `src.orchestrator.FinSightOrchestrator`.

---

### Command-Line Interface

**Basic usage:**
```bash
python -m src.main --transcript <PATH> --ticker <SYMBOL>
```

**With custom query:**
```bash
python -m src.main \
  --transcript data/input/transcript.txt \
  --ticker GOOGL \
  --query "Focus on AI initiatives and revenue impact"
```

**With custom output directory:**
```bash
python -m src.main \
  --transcript data/input/transcript.txt \
  --ticker AAPL \
  --output ./my_reports
```

### CLI Options

```
Required:
  -t, --transcript PATH    Path to earnings call transcript (.txt format)
  -s, --ticker SYMBOL      Company ticker symbol (e.g., GOOGL, AAPL)

Optional:
  -q, --query TEXT         Custom analysis query
  -o, --output DIR         Output directory for reports (default: data/output)
```

### Programmatic Usage

```python
from src.orchestrator import FinSightOrchestrator

# Initialize orchestrator
orchestrator = FinSightOrchestrator()

# Run analysis
result = orchestrator.run_analysis(
    transcript_path="data/input/transcript.txt",
    ticker="GOOGL",
    user_query="Comprehensive financial analysis"  # Optional
)

# Access individual results
sentiment = result['sentiment_result']
print(f"Sentiment: {sentiment.overall_sentiment}")
print(f"Score: {sentiment.sentiment_score}")
print(f"Confidence: {sentiment.confidence}")

events = result['event_detection_result']
print(f"Events detected: {events.total_events_found}")

volatility = result['volatility_result']
print(f"Predicted volatility: {volatility.predicted_volatility}")

# Access final report
final_report = result['final_report']
```

### Demo Mode

Run an interactive demonstration:

```bash
python demo.py
```

This will:
- Check prerequisites
- Run a complete analysis on sample data
- Display results summary
- Show generated reports

---

## Architecture

### Multi-Agent System with Metacognitive Guardrails

FinSight employs 4 specialized agents with runtime metacognition and self-assessment:

```
┌─────────────────────────────────────────────────────────┐
│                    USER INPUT                           │
│  📄 Transcript Path + 🏢 Ticker Symbol                   │
└────────────────────┬────────────────────────────────────┘
                     ↓
┌────────────────────────────────────────────────────────┐
│         🧠 COORDINATOR AGENT                           │
│    (Metacognitive Planning & Orchestration)            │
│  • Interprets query with self-awareness                │
│  • Creates analysis plan                               │
│  • Self-scores confidence in understanding             │
│  • Orchestrates agents based on self-model             │
│  📊 LLM-as-Judge: Confidence Score (0-1)               │
└────────────────────┬───────────────────────────────────┘
                     ↓
┌────────────────────────────────────────────────────────┐
│              📄 LOAD TRANSCRIPT                        │
└────────────────────┬───────────────────────────────────┘
                     ↓
        ┌────────────┼────────────┐
        ↓            ↓             ↓
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ 😊 SENTIMENT │ │ 🔍 EVENT      │ │ 📊 VOLATILITY│
│    AGENT     │ │  DETECTION   │ │  PREDICTION  │
│              │ │    AGENT     │ │    AGENT     │
│      ↓       │ │      ↓       │ │      ↓       │
│   Tavily     │ │  SEC EDGAR   │ │  yfinance    │
│   News       │ │  Filings     │ │  Market Data │
│      ↓       │ │      ↓       │ │      ↓       │
│  ANALYZE     │ │  ANALYZE     │ │  ANALYZE     │
│      ↓       │ │      ↓       │ │      ↓       │
│ 🔍 SELF-EVAL │ │ 🔍 SELF-EVAL  │ │ 🔍 SELF-EVAL │
│ Confidence   │ │ Confidence   │ │ Confidence   │
│ vs Threshold │ │ vs Threshold │ │ vs Threshold │
│  (≥65%)      │ │  (≥70%)      │ │  (≥60%)      │
│      ↓       │ │      ↓       │ │      ↓       │
│   Report     │ │   Report     │ │   Report     │
└──────────────┘ └──────────────┘ └──────────────┘
        │            │             │
        └────────────┼─────────────┘
                     ↓
┌────────────────────────────────────────────────────────┐
│       📝 SYNTHESIZE FINAL REPORT                       │
│  • Combines all findings                               │
│  • Validates against self-model guardrails             │
│  • Checks confidence scores vs thresholds              │
│  • Tracks and reports guardrail violations             │
│  • Generates comprehensive report with transparency    │
└────────────────────────────────────────────────────────┘
```

### Data Flow

1. **User Input** → Transcript path + ticker symbol
2. **Coordinator** → Plans analysis workflow
3. **Load Transcript** → Reads and validates file
4. **Agent Execution** → Sequential processing:
   - Sentiment Agent → Tavily validation → Report
   - Event Agent → SEC EDGAR validation → Report
   - Volatility Agent → yfinance validation → Report
5. **Report Synthesis** → Comprehensive final report
6. **Output** → 4 markdown files saved to `data/output/`

---

## Metacognitive Self-Model & LLM-as-Judge

### Overview

FinSight implements **runtime metacognition** and **LLM-as-Judge** patterns as core guardrail mechanisms. The system maintains self-awareness of its capabilities, limitations, and confidence levels throughout execution.

### Self-Model Architecture

The system maintains a comprehensive self-model (`FinSightSelfModel`) that includes:

```python
FinSightSelfModel:
  ├── Mission: System's core purpose and goals
  ├── Agent Capabilities: What each agent can/cannot do
  │   ├── Capabilities list
  │   ├── Limitations list
  │   └── Confidence threshold (guardrail)
  ├── Operating Boundaries: Hard limits and ethical constraints
  ├── Active Guardrails: Runtime checks and validations
  └── Guardrail Violations: Tracked incidents
```

### LLM-as-Judge: Confidence Scoring

Each agent implements **self-evaluation** by scoring its own findings:

#### 1. Coordinator Self-Assessment
```python
MetacognitiveDecision:
  ├── user_intent: Understood goal
  ├── analysis_plan: Step-by-step approach
  ├── agents_to_invoke: Selected specialists
  ├── confidence: Self-scored (0-1)  ← LLM judges itself
  └── reasoning: Explanation of plan
```

#### 2. Agent Self-Scoring During Execution

Each specialized agent scores its confidence:

| Agent | Self-Scores | Threshold | Guardrail Action |
|-------|------------|-----------|------------------|
| **Sentiment** | Sentiment confidence (0-1) | ≥65% | Flag if below threshold |
| **Event Detection** | Event confidence (0-1) | ≥70% | Flag if below threshold |
| **Volatility** | Prediction confidence (0-1) | ≥60% | Flag if below threshold |

#### 3. Runtime Guardrail Enforcement

```
┌─────────────────────────────────────────────────┐
│  Agent completes analysis                       │
│  ↓                                              │
│  Agent scores own confidence (LLM-as-Judge)     │
│  ↓                                              │
│  Compare: confidence >= threshold?              │
│  ├─ YES → ✓ Pass guardrail check                │
│  └─ NO  → ⚠ Record guardrail violation          │
│     ↓                                           │
│     Add to guardrails_applied list              │
│     ↓                                           │
│     Include warning in final report             │
└─────────────────────────────────────────────────┘
```

### Metacognitive Flow Diagram

```
┌──────────────────────────────────────────────────────────┐
│                     SYSTEM START                         │
│              Load FinSightSelfModel                      │
│   (Mission, Capabilities, Boundaries, Thresholds)        │
└───────────────────────┬──────────────────────────────────┘
                        ↓
┌──────────────────────────────────────────────────────────┐
│               COORDINATOR (Metacognitive)                │
│  1. Analyze user query                                   │
│  2. Plan analysis approach                               │
│  3. Self-score: confidence in understanding              │
│  4. Check: confidence meets expectations?                │
│     └─ Record decision reasoning                         │
└───────────────────────┬──────────────────────────────────┘
                        ↓
┌──────────────────────────────────────────────────────────┐
│                  FOR EACH AGENT:                         │
│  ┌────────────────────────────────────────────────────┐  │
│  │ 1. Execute Analysis (with external tool validation)│  │
│  │    ├─ Sentiment: Analyze + Tavily news             │  │
│  │    ├─ Events: Detect + SEC EDGAR filings           │  │
│  │    └─ Volatility: Predict + yfinance data          │  │
│  └────────────────────┬───────────────────────────────┘  │
│                       ↓                                  │
│  ┌────────────────────────────────────────────────────┐  │
│  │ 2. LLM-as-Judge: Self-Score Confidence             │  │
│  │    - Agent evaluates own findings                  │  │
│  │    - Produces confidence score (0-1)               │  │
│  │    - Example: "I am 72% confident in this result"  │  │
│  └────────────────────┬───────────────────────────────┘  │
│                       ↓                                  │
│  ┌────────────────────────────────────────────────────┐  │
│  │ 3. Guardrail Check (Runtime)                       │  │
│  │    Compare: agent_confidence >= threshold?         │  │
│  │    ├─ Sentiment: >= 65%?                           │  │
│  │    ├─ Events: >= 70%?                              │  │
│  │    └─ Volatility: >= 60%?                          │  │
│  └────────────────────┬───────────────────────────────┘  │
│                       ↓                                  │
│               ┌──────────────────┐                       │
│               │ Below threshold? │                       │
│               └────┬─────────┬───┘                       │
│                YES ↓         ↓ NO                        │
│     ┌──────────────────┐   ✓ Continue                    │
│     │ Record Violation │                                 │
│     │ - Timestamp      │                                 │
│     │ - Agent name     │                                 │
│     │ - Guardrail type │                                 │
│     │ - Description    │                                 │
│     │ - Action taken   │                                 │
│     └──────────────────┘                                 │
└───────────────────────┬──────────────────────────────────┘
                        ↓
┌──────────────────────────────────────────────────────────┐
│              SYNTHESIZE FINAL REPORT                     │
│  1. Combine all agent findings                           │
│  2. Include metacognitive analysis                       │
│  3. Display confidence summary table:                    │
│     ┌────────────┬────────────┬───────────┬─────────┐    │
│     │ Agent      │ Confidence │ Threshold │ Status  │    │
│     ├────────────┼────────────┼───────────┼─────────┤    │
│     │ Sentiment  │ 72%        │ 65%       │ ✓ Pass  │    │
│     │ Events     │ 68%        │ 70%       │ ⚠ Low   │    │
│     │ Volatility │ 75%        │ 60%       │ ✓ Pass  │    │
│     └────────────┴────────────┴───────────┴─────────┘    │
│  4. Report guardrail violations (if any)                 │
│  5. Include system boundaries and disclaimers            │
└──────────────────────────────────────────────────────────┘
```

### Key Benefits

✅ **Transparent Uncertainty** - Every output includes confidence scores  
✅ **Runtime Validation** - Agents self-assess before committing results  
✅ **Automated Quality Control** - Threshold guardrails catch low-confidence outputs  
✅ **Audit Trail** - All self-assessments and guardrail checks are logged  
✅ **Metacognitive Reasoning** - Coordinator explains its decision-making process

### Code Implementation

The self-model and confidence checks are defined in `src/models.py`:

```python
class FinSightSelfModel(BaseModel):
    """Metacognitive self-model for runtime guardrails."""
    system_name: str = "FinSight Agent"
    mission: str
    agent_capabilities: List[AgentCapability]  # Each has confidence_threshold
    operating_boundaries: List[str]
    active_guardrails: List[str]
    guardrail_violations: List[GuardrailViolation]

class AgentCapability(BaseModel):
    """Agent self-awareness: what it can/cannot do."""
    agent_name: str
    capabilities: List[str]
    limitations: List[str]
    confidence_threshold: float  # Guardrail threshold
```

Example confidence check in final report synthesis (from `src/orchestrator.py`):

```python
# Check agent confidence against self-model threshold
threshold = self_model.agent_capabilities[0].confidence_threshold
if sentiment.confidence >= threshold:
    status = "✓ Pass"
else:
    status = "⚠ Low"
    # Could trigger guardrail violation recording
```

---

## Output Reports

The system generates 4 markdown reports per analysis:

### 1. Sentiment Analysis Report
**Filename:** `sentiment_[TICKER]_[TIMESTAMP].md`

**Contents:**
- Overall sentiment classification (very_positive/positive/neutral/negative/very_negative)
- Numerical sentiment score (-1.0 to 1.0)
- Market sentiment summary
- Key sentiment drivers
- News headlines analyzed (from Tavily)
- Tool validations performed
- Confidence metrics

### 2. Event Detection Report
**Filename:** `event_detection_[TICKER]_[TIMESTAMP].md`

**Contents:**
- List of significant events detected
- Event descriptions and types
- Verification status (mentioned in call, verified)
- Impact assessments (high/medium/low)
- SEC filing references (8-K, 10-Q, 10-K)
- Tool validations performed
- Confidence metrics

### 3. Volatility Prediction Report
**Filename:** `volatility_[TICKER]_[TIMESTAMP].md`

**Contents:**
- Predicted volatility level (very_high/high/moderate/low/very_low)
- Volatility score (0.0 to 1.0)
- Historical volatility comparison
- Key volatility drivers
- Transcript insights (answers to analysis questions)
- Sentiment impact analysis
- Event impact analysis
- Tool validations performed
- Confidence metrics

### 4. Final Comprehensive Report
**Filename:** `final_report_[TICKER]_[TIMESTAMP].md`

**Contents:**
- Executive summary
- Coordinator's metacognitive analysis
- Complete sentiment analysis
- Complete event detection
- Complete volatility prediction
- Guardrails applied
- Confidence summary table
- System disclaimers

---

## Project Structure

```
finsight-agent/
├── src/                          # Main source code
│   ├── __init__.py              # Package initialization
│   ├── config.py                # Configuration management
│   ├── models.py                # Pydantic data models
│   ├── tools.py                 # External tool integrations
│   ├── orchestrator.py          # LangGraph workflow orchestrator
│   ├── main.py                  # CLI entry point
│   └── agents/                  # Agent implementations
│       ├── __init__.py
│       ├── base.py              # Base agent class
│       ├── coordinator.py       # Coordinator agent
│       ├── sentiment.py         # Sentiment analysis agent
│       ├── events.py            # Event detection agent
│       └── volatility.py        # Volatility prediction agent
│
├── data/                         # Data directories
│   ├── input/                   # Input transcripts
│   ├── output/                  # Generated reports (gitignored)
│   └── sec_filings/             # SEC filings cache (gitignored)
│
├── app.py                        # 🚀 Streamlit web interface
├── api.py                        # Stubbed API for Streamlit POC
├── test_api.py                   # API stub testing script
├── run_streamlit.sh              # Streamlit launcher script
├── .streamlit/                   # Streamlit configuration
│   └── config.toml              # UI theme and settings
│
├── demo.py                       # Interactive demo script
├── examples.py                   # Programmatic usage examples
├── test_setup.py                 # Setup verification script
├── prepare_transcript.py         # Transcript preparation utility
├── run_test.sh                   # Quick test script
│
├── pyproject.toml               # Project metadata and dependencies
├── requirements.txt             # Pip requirements (includes streamlit)
├── .env.example                 # Environment template
├── .gitignore                   # Git ignore rules
│
├── README.md                    # This file (main documentation)
├── CHANGELOG.md                 # Version history and changes
├── CODE_OF_CONDUCT.md           # Community guidelines
└── CONTRIBUTING.md              # Contribution guidelines
```

---

## Agent Details

### 1. Coordinator Agent (Metacognitive)

**Role:** Metacognitive planning, orchestration, and self-assessment

**Capabilities:**
- Interprets user queries with self-awareness
- Creates detailed analysis plans
- Determines which agents to invoke
- **Self-scores confidence** in understanding (LLM-as-Judge)
- Provides explicit reasoning for decisions

**Metacognitive Process:**
```python
1. Analyze user query
2. Determine user intent
3. Create step-by-step analysis plan
4. Select appropriate specialized agents
5. 🔍 SELF-ASSESS: Score confidence in understanding (0-1)
6. Provide transparent reasoning
7. Return structured MetacognitiveDecision
```

**Output:** `MetacognitiveDecision` with plan, confidence, and reasoning

**Self-Assessment Example:**
```python
MetacognitiveDecision(
    user_intent="Comprehensive financial analysis",
    analysis_plan=["Step 1...", "Step 2...", ...],
    agents_to_invoke=["sentiment_analysis", "event_detection", "volatility_prediction"],
    confidence=0.85,  # ← Coordinator judges itself at 85% confident
    reasoning="User query is clear and comprehensive. All three agents needed..."
)
```

---

### 2. Sentiment Analysis Agent

**Role:** Analyze sentiment from transcript and validate with market news

**Tool:** Tavily Search API

**Capabilities:**
- Extract sentiment from transcript
- Search recent financial news
- Compare transcript vs. market sentiment
- Identify sentiment drivers
- **Self-score confidence** using LLM-as-Judge

**Process:**
```python
1. Extract sentiment from transcript
2. Search Tavily for recent news (5 articles)
3. Analyze market sentiment
4. Compare transcript vs. news sentiment
5. Generate sentiment classification
6. Calculate sentiment score (-1.0 to 1.0)
7. 🔍 SELF-ASSESS: Score confidence in sentiment analysis (0-1)
8. ✓ GUARDRAIL CHECK: confidence >= 65%?
9. Save sentiment report with confidence score
```

**Output:** `SentimentAnalysisResult` with classification, score, validations, and **self-scored confidence**

**Confidence Threshold (Guardrail):** ≥65%

**Self-Assessment Example:**
```python
SentimentAnalysisResult(
    overall_sentiment="positive",
    sentiment_score=0.72,
    confidence=0.68,  # ← Agent judges itself at 68% confident
    market_sentiment="Generally positive market reaction...",
    key_sentiment_drivers=["Revenue growth", "AI initiatives"],
    tool_validations=["Validated with 5 Tavily news articles"]
)
# Guardrail: 68% >= 65% ✓ Pass
```

---

### 3. Event Detection Agent

**Role:** Identify significant corporate events and verify with official filings

**Tool:** SEC EDGAR Downloader

**Capabilities:**
- Detect events from transcript
- Download SEC filings (8-K, 10-Q, 10-K)
- Verify events against official sources
- Assess event materiality
- **Self-score confidence** using LLM-as-Judge

**Process:**
```python
1. Identify significant events in transcript
2. Download recent SEC filings (8-K, 10-Q)
3. Cross-reference events with filings
4. Verify event details
5. Assess impact (high/medium/low)
6. 🔍 SELF-ASSESS: Score confidence in event detection (0-1)
7. ✓ GUARDRAIL CHECK: confidence >= 70%?
8. Save event detection report with confidence score
```

**Output:** `SignificantEventDetectionResult` with events, validations, and **self-scored confidence**

**Confidence Threshold (Guardrail):** ≥70% (Highest threshold due to verification requirements)

**Self-Assessment Example:**
```python
SignificantEventDetectionResult(
    events=[...],
    total_events_found=3,
    verified_count=2,
    confidence=0.75,  # ← Agent judges itself at 75% confident
    tool_validations=["Verified against SEC 8-K filings", "Cross-referenced 10-Q"]
)
# Guardrail: 75% >= 70% ✓ Pass
```

---

### 4. Volatility Prediction Agent

**Role:** Predict stock volatility using multi-modal analysis

**Tool:** yfinance API

**Capabilities:**
- Answer structured questions from transcript
- Retrieve historical volatility data
- Analyze price movements
- Integrate sentiment and event data from other agents
- **Self-score confidence** using LLM-as-Judge

**Process:**
```python
1. Answer analysis questions from transcript
2. Get historical volatility (1-month) from yfinance
3. Get price movement data
4. Retrieve stock information
5. Integrate sentiment results from Sentiment Agent
6. Integrate event results from Event Detection Agent
7. Predict future volatility (multi-modal synthesis)
8. Calculate volatility score (0.0 to 1.0)
9. 🔍 SELF-ASSESS: Score confidence in prediction (0-1)
10. ✓ GUARDRAIL CHECK: confidence >= 60%?
11. Save volatility report with confidence score
```

**Output:** `VolatilityPredictionResult` with prediction, validations, and **self-scored confidence**

**Confidence Threshold (Guardrail):** ≥60% (Lower threshold due to inherent prediction uncertainty)

**Self-Assessment Example:**
```python
VolatilityPredictionResult(
    predicted_volatility="moderate",
    volatility_score=0.48,
    confidence=0.65,  # ← Agent judges itself at 65% confident
    historical_volatility=0.22,
    sentiment_impact="Positive sentiment reduces expected volatility",
    event_impact="2 high-impact events increase volatility",
    tool_validations=["Historical data from yfinance (30 days)"]
)
# Guardrail: 65% >= 60% ✓ Pass
```

---

## Tool Integration

### Tool Usage Matrix

| Agent | External Tool | Purpose | API Calls |
|-------|--------------|---------|-----------|
| **Sentiment** | Tavily Search API | Validate sentiment with recent news | 1-2 calls |
| **Event Detection** | SEC EDGAR Downloader | Verify events with official filings | 1-3 downloads |
| **Volatility** | yfinance API | Validate predictions with market data | 2-3 calls |

### Tool Details

#### 1. Tavily Search API (Sentiment Agent)

**What it does:**
- Searches recent financial news
- Filters for earnings and sentiment-related articles
- Returns up to 5 relevant articles

**Usage in code:**
```python
from src.tools import news_search_tool

# Get sentiment-relevant news
results = news_search_tool.get_sentiment_news(ticker="GOOGL")
headlines = [r['title'] for r in results]
```

#### 2. SEC EDGAR Downloader (Event Agent)

**What it does:**
- Downloads official SEC filings
- Focuses on 8-K (material events), 10-Q (quarterly), 10-K (annual)
- Caches filings locally

**Usage in code:**
```python
from src.tools import sec_filing_tool

# Download recent filings
results = sec_filing_tool.download_recent_filings(
    ticker="GOOGL",
    filing_types=["8-K", "10-Q"],
    limit=3
)
```

#### 3. yfinance API (Volatility Agent)

**What it does:**
- Retrieves historical stock data
- Calculates volatility metrics
- Gets price movement statistics

**Usage in code:**
```python
from src.tools import market_data_tool

# Get historical volatility
volatility = market_data_tool.get_historical_volatility(
    ticker="GOOGL",
    period="1mo"
)

# Get price movement
movement = market_data_tool.get_price_movement(
    ticker="GOOGL",
    period="1mo"
)
```

---

## Guardrails & Safety

### Overview

FinSight implements **runtime metacognitive guardrails** powered by the self-model and LLM-as-Judge patterns. Unlike static rule-based systems, these guardrails involve the AI reasoning about its own capabilities and confidence during execution.

### Active Guardrails (Runtime)

#### 1. **Confidence Threshold Enforcement** (LLM-as-Judge)
- **Mechanism**: Each agent self-scores confidence in its findings (0-1)
- **Check**: Runtime comparison against agent-specific thresholds
- **Action**: Below-threshold results trigger warnings and are flagged in reports
- **Implementation**: Confidence scores embedded in structured outputs (Pydantic models)

**Example Flow:**
```python
# Agent generates result with self-assessment
result = SentimentAnalysisResult(
    overall_sentiment="positive",
    sentiment_score=0.72,
    confidence=0.68,  # LLM judges itself at 68% confident
    ...
)

# Runtime guardrail check
if result.confidence < threshold (0.65):
    record_guardrail_violation(...)
```

#### 2. **Source Verification Requirement**
- **Mechanism**: All findings must cite external validation sources
- **Check**: `tool_validations` field must be populated
- **Action**: Reports show which tools validated each finding
- **Transparency**: Clear audit trail in every report

#### 3. **Investment Advice Prohibition** (Self-Model Boundary)
- **Mechanism**: System self-model defines operating boundaries
- **Check**: Coordinator is aware of this boundary during planning
- **Action**: Explicitly avoids stock recommendations in all outputs
- **Purpose**: Legal/ethical compliance, educational use only

#### 4. **Transparent Limitation Disclosure** (Metacognitive Awareness)
- **Mechanism**: Each agent declares its limitations in the self-model
- **Check**: Limitations included in `AgentCapability` definitions
- **Action**: All reports include disclaimers and confidence levels
- **Purpose**: User awareness of system boundaries

### Confidence Thresholds (Guardrail Parameters)

| Agent | Threshold | Purpose | Defined In |
|-------|-----------|---------|------------|
| Sentiment Analysis | **≥65%** | Minimum for sentiment claims | `AgentCapability.confidence_threshold` |
| Event Detection | **≥70%** | Minimum for event verification | `AgentCapability.confidence_threshold` |
| Volatility Prediction | **≥60%** | Minimum for volatility predictions | `AgentCapability.confidence_threshold` |

**These thresholds are part of the self-model and can be adjusted based on use case risk tolerance.**

### Operating Boundaries (Self-Model Constraints)

These boundaries are encoded in the system's self-model and inform agent behavior:

✗ NO personalized investment advice  
✗ NO stock buy/sell recommendations  
✗ NO guarantees about future performance  
✓ Educational and analytical purposes ONLY  
✓ Must disclose all confidence levels  
✓ Must cite all sources  

### Guardrail Tracking & Runtime Monitoring

All guardrail checks are **actively monitored during execution** and reported in the final report.

#### Guardrail Violation Structure

When confidence falls below threshold:

```python
GuardrailViolation(
    timestamp: "2025-01-15 14:32:10",
    agent: "Event Detection Agent",
    guardrail_type: "Confidence Threshold",
    description: "Confidence 68% below threshold 70%",
    action_taken: "Flagged in report, included with warning"
)
```

#### Example Report Output (No Violations)

```markdown
## 5. Guardrails and System Boundaries

**Guardrail Checks Performed:** 0

*All confidence thresholds met. No guardrail violations detected.*

**Active Guardrails:**
- Confidence threshold enforcement
- Source verification requirement
- Investment advice prohibition
- Transparent limitation disclosure

**Operating Boundaries:**
- NO personalized investment advice or stock recommendations
- NO guarantees about future stock performance
- All outputs are for educational and analytical purposes only
- Must disclose confidence levels and limitations
```

#### Example Report Output (With Violations)

```markdown
## 5. Guardrails and System Boundaries

**Guardrail Checks Performed:** 1

- **Confidence Threshold** (Event Detection Agent)
  - Confidence 68% fell below required threshold of 70%
  - Action: Flagged in report with low-confidence warning

**Active Guardrails:**
- Confidence threshold enforcement ← *TRIGGERED*
- Source verification requirement
- Investment advice prohibition
- Transparent limitation disclosure
```

#### Confidence Summary Table (LLM-as-Judge Results)

Every final report includes a table showing how each agent scored itself:

```markdown
## 6. System Confidence Summary

| Agent | Confidence | Threshold | Status |
|-------|-----------|-----------|--------|
| Sentiment Analysis | 72% | 65% | ✓ Pass |
| Event Detection | 68% | 70% | ⚠ Low  |
| Volatility Prediction | 75% | 60% | ✓ Pass |
```

This transparency allows users to assess the reliability of each component independently.

---

## Configuration & Customization

### Custom Analysis Questions

Edit `src/models.py` to customize questions:

```python
DEFAULT_ANALYSIS_QUESTIONS = [
    AnalysisQuestion(
        category="Financial Performance",
        focus_item="Revenue Growth",
        question="What was the year-over-year revenue growth rate?",
        priority="high"
    ),
    AnalysisQuestion(
        category="Strategic Initiatives",
        focus_item="Key Projects",
        question="What are the key projects or initiatives?",
        priority="high"
    ),
    # Add your custom questions here
    AnalysisQuestion(
        category="Your Category",
        focus_item="Your Focus",
        question="Your specific question?",
        priority="high"
    ),
]
```

### Adjust Confidence Thresholds

Edit `src/models.py`:

```python
AgentCapability(
    agent_name="Sentiment Analysis Agent",
    capabilities=[...],
    limitations=[...],
    confidence_threshold=0.65  # Adjust as needed
)
```

### Change Model Parameters

Edit `src/config.py`:

```python
@dataclass
class ScalewayConfig:
    model: str = "qwen3-235b-a22b-instruct-2507"
    temperature: float = 0.0      # Adjust for creativity
    max_tokens: int = 2048         # Adjust for response length
```

### Custom Output Directory

Specify via CLI:

```bash
python -m src.main \
  --transcript transcript.txt \
  --ticker GOOGL \
  --output ./custom_reports
```

Or programmatically:

```python
from src.config import config

config.paths.output_dir = "./custom_reports"
```

---

## Troubleshooting

### Import Errors

**Problem:** `ModuleNotFoundError` or import errors

**Solution:**
```bash
pip install -r requirements.txt
```

Verify all packages are installed:
```bash
python -c "import pydantic, langchain_core, langgraph, yfinance; print('OK')"
```

### Configuration Errors

**Problem:** "Missing required environment variables"

**Solution:**
1. Ensure `.env` file exists:
   ```bash
   cp .env.example .env
   ```

2. Verify all required keys are set:
   ```bash
   cat .env
   ```

3. Check for extra spaces or quotes in values

4. Test configuration:
   ```bash
   python -c "from src.config import config; config.validate(); print('OK')"
   ```

### Transcript Not Found

**Problem:** "Error: Transcript file not found"

**Solution:**
1. Verify file path:
   ```bash
   ls -l data/input/
   ```

2. Use absolute path:
   ```bash
   python -m src.main --transcript /full/path/to/transcript.txt --ticker GOOGL
   ```

3. Ensure file is .txt format (not PDF or other)

### API Errors

**Problem:** API connection or authentication errors

**Solution:**

**For Scaleway:**
- Verify project ID and secret key are correct
- Check project has GenAI API enabled
- Ensure API quota not exceeded

**For Tavily:**
- Verify API key is valid
- Check rate limits (free tier: 1000 searches/month)
- Ensure internet connection

**For yfinance:**
- Usually no auth needed
- Check internet connection
- Try different ticker symbol

**Test each API:**
```bash
# Test Tavily
python -c "from langchain_community.tools.tavily_search import TavilySearchResults; tool = TavilySearchResults(api_key='YOUR_KEY'); print(tool.invoke('test'))"

# Test yfinance
python -c "import yfinance as yf; print(yf.Ticker('GOOGL').info['longName'])"
```

### Out of Memory

**Problem:** System runs out of memory

**Solution:**
- Reduce `max_tokens` in `src/config.py`
- Process shorter transcript excerpts
- Close other applications
- Use a machine with more RAM

### Slow Performance

**Problem:** Analysis takes too long

**Solution:**
- Check internet connection
- Reduce number of analysis questions
- Use shorter transcripts for testing
- Consider local caching of API results

---

## Development

### Adding New Agents

1. **Create agent file** in `src/agents/`:
   ```python
   # src/agents/my_agent.py
   from .base import BaseAgent
   from ..models import MyAgentResult
   
   class MyAgent(BaseAgent):
       def __init__(self):
           super().__init__("My Agent")
       
       def process(self, state):
           # Your agent logic here
           return {"my_result": result}
   ```

2. **Add to `src/agents/__init__.py`:**
   ```python
   from .my_agent import MyAgent
   
   __all__ = [..., "MyAgent"]
   ```

3. **Define output model** in `src/models.py`:
   ```python
   class MyAgentResult(BaseModel):
       field1: str
       field2: int
       confidence: float
   ```

4. **Update orchestrator** in `src/orchestrator.py`:
   ```python
   self.my_agent = MyAgent()
   
   workflow.add_node("my_agent", self._my_agent_node)
   workflow.add_edge("previous_node", "my_agent")
   ```

### Adding New Tools

1. **Create tool class** in `src/tools.py`:
   ```python
   class MyTool:
       def __init__(self, api_key: str):
           self.api_key = api_key
       
       def fetch_data(self, query: str):
           # Tool logic here
           pass
   ```

2. **Initialize globally**:
   ```python
   my_tool = MyTool(config.api.my_api_key)
   ```

3. **Use in agents**:
   ```python
   from ..tools import my_tool
   
   data = my_tool.fetch_data("query")
   ```

### Running Tests

Currently, the system includes:

```bash
# Setup verification
python test_setup.py

# Interactive demo
python demo.py

# Quick test script
./run_test.sh
```

**Future:** Unit tests and integration tests (TODO)

### Code Style

- Follow PEP 8
- Use type hints
- Document with docstrings
- Use Pydantic for data validation

---

## Examples

### Example 1: Basic Analysis

```python
from src.orchestrator import FinSightOrchestrator

orchestrator = FinSightOrchestrator()
result = orchestrator.run_analysis(
    transcript_path="data/input/Alphabet_2025_Q1_Earnings_Call_complete_transcript.txt",
    ticker="GOOGL"
)
```

### Example 2: Custom Query

```python
from src.orchestrator import FinSightOrchestrator

orchestrator = FinSightOrchestrator()
result = orchestrator.run_analysis(
    transcript_path="data/input/transcript.txt",
    ticker="GOOGL",
    user_query="Focus on AI initiatives and their impact on revenue growth"
)
```

### Example 3: Accessing Results

```python
from src.orchestrator import FinSightOrchestrator

orchestrator = FinSightOrchestrator()
result = orchestrator.run_analysis(
    transcript_path="data/input/transcript.txt",
    ticker="GOOGL"
)

# Access sentiment
if result.get('sentiment_result'):
    sent = result['sentiment_result']
    print(f"Sentiment: {sent.overall_sentiment}")
    print(f"Score: {sent.sentiment_score:.2f}")
    print(f"Confidence: {sent.confidence:.2%}")
    print(f"News analyzed: {len(sent.news_headlines)}")

# Access events
if result.get('event_detection_result'):
    events = result['event_detection_result']
    print(f"\nEvents detected: {events.total_events_found}")
    print(f"Verified: {events.verified_count}")
    for event in events.events:
        print(f"- {event.event_type}: {event.description[:50]}...")

# Access volatility
if result.get('volatility_result'):
    vol = result['volatility_result']
    print(f"\nPredicted volatility: {vol.predicted_volatility}")
    print(f"Score: {vol.volatility_score:.2f}")
    print(f"Historical: {vol.historical_volatility:.2%}")
```

### Example 4: Command-Line Variations

```bash
# Basic
python -m src.main -t data/input/transcript.txt -s GOOGL

# Custom query
python -m src.main \
  -t data/input/transcript.txt \
  -s AAPL \
  -q "Analyze product announcements and their market impact"

# Custom output directory
python -m src.main \
  -t data/input/transcript.txt \
  -s MSFT \
  -o ./quarterly_reports/Q1_2025

# Help
python -m src.main --help
```

---

## Dependencies

### Core Libraries

- **pydantic (≥2.12.3)** - Data validation and modeling
- **langchain-core (≥1.0.2)** - LLM orchestration framework
- **langchain-openai (≥1.0.1)** - OpenAI-compatible API client
- **langchain-community (≥0.4.1)** - Community tools (Tavily)
- **langgraph (≥0.2.0)** - Multi-agent workflow graphs
- **yfinance (≥0.2.66)** - Market data retrieval
- **sec-edgar-downloader (≥5.0.3)** - SEC filing access
- **python-dotenv (≥1.0.0)** - Environment configuration
- **typing-extensions (≥4.9.0)** - Type hints

### Full Requirements

See `requirements.txt` for complete list:

```bash
cat requirements.txt
```

### Installing Dependencies

```bash
pip install -r requirements.txt
```

Or with UV:

```bash
uv pip install -e .
```

---

## License

Apache License 2.0 - See [LICENSE](LICENSE) file for details

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute to this project.

---

## Disclaimers

⚠️ **IMPORTANT: This system is for educational and informational purposes only.**

This system does NOT constitute:
- Investment advice
- Financial recommendations
- Guarantees about future stock performance
- Professional financial guidance

**Key Points:**
- All investments involve risk, including possible loss of principal
- Past performance does not guarantee future results
- The system's predictions and analyses should not be the sole basis for investment decisions
- Consult with qualified financial professionals before making any investment decisions
- The creators and contributors are not liable for any financial losses

**Data Sources:**
- External APIs (Tavily, SEC EDGAR, yfinance) may have limitations or delays
- Information accuracy depends on source data quality
- Always verify critical information with official sources

---

## Support

For issues, questions, or feature requests:

1. Check this README for solutions
2. Run `python test_setup.py` to verify configuration
3. Try `python demo.py` for a working example
4. Review `examples.py` for usage patterns
5. Open an issue on GitHub

---

## Acknowledgments

Built using:
- **Scaleway GenAI** for LLM inference
- **LangChain** and **LangGraph** for orchestration
- **Tavily** for news search
- **SEC EDGAR** for official filings
- **yfinance** for market data

---

**FinSight Agent v1.0** - Metacognitive Multi-Agent Financial Analysis System

*Generated with 🤖 precision and 📊 financial insights*
