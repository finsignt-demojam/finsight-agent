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

FinSight Agent is a production-ready multi-agent system that analyzes earnings call transcripts using:

- **4 Specialized Agents**: Coordinator, Sentiment Analysis, Event Detection, and Volatility Prediction
- **External Tool Validation**: Tavily news search, SEC EDGAR filings, and yfinance market data
- **Metacognitive Reasoning**: Self-aware decision-making and performance assessment
- **Individual Reports**: Separate markdown outputs for each agent plus comprehensive final report
- **Guardrail System**: Confidence thresholds, source verification, and transparent limitations

### Key Features

✅ **Multi-Agent Orchestration** - LangGraph-based workflow with metacognitive coordinator  
✅ **Tool-Enhanced Validation** - Each agent uses external APIs to verify findings  
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

### Multi-Agent System

FinSight employs 4 specialized agents:

```
┌─────────────────────────────────────────────────────────┐
│                    USER INPUT                           │
│  📄 Transcript Path + 🏢 Ticker Symbol                  │
└────────────────────┬────────────────────────────────────┘
                     ↓
┌────────────────────────────────────────────────────────┐
│         🧠 COORDINATOR AGENT                           │
│    (Metacognitive Planning & Orchestration)            │
│  • Interprets query                                    │
│  • Creates analysis plan                               │
│  • Orchestrates agents                                 │
└────────────────────┬───────────────────────────────────┘
                     ↓
┌────────────────────────────────────────────────────────┐
│              📄 LOAD TRANSCRIPT                        │
└────────────────────┬───────────────────────────────────┘
                     ↓
        ┌────────────┼────────────┐
        ↓            ↓             ↓
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ 😊 SENTIMENT │ │ 🔍 EVENT     │ │ 📊 VOLATILITY│
│    AGENT     │ │  DETECTION   │ │  PREDICTION  │
│              │ │    AGENT     │ │    AGENT     │
│      ↓       │ │      ↓       │ │      ↓       │
│   Tavily    │ │  SEC EDGAR   │ │  yfinance    │
│   News      │ │  Filings     │ │  Market Data │
│      ↓       │ │      ↓       │ │      ↓       │
│   Report    │ │   Report     │ │   Report     │
└──────────────┘ └──────────────┘ └──────────────┘
        │            │             │
        └────────────┼─────────────┘
                     ↓
┌────────────────────────────────────────────────────────┐
│       📝 SYNTHESIZE FINAL REPORT                       │
│  • Combines all findings                              │
│  • Applies guardrails                                 │
│  • Generates comprehensive report                     │
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
│   │   ├── Alphabet_2025_Q1_Earnings_Call_complete_transcript.txt
│   │   └── GOOG_2025_Q3_Earnings_Transcript.txt
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

### 1. Coordinator Agent

**Role:** Metacognitive planning and orchestration

**Capabilities:**
- Interprets user queries
- Creates detailed analysis plans
- Determines which agents to invoke
- Provides reasoning and confidence

**Process:**
```python
1. Analyze user query
2. Determine user intent
3. Create analysis plan
4. Select agents to invoke
5. Assess confidence in plan
6. Provide reasoning
```

**Output:** `MetacognitiveDecision` with plan and confidence

---

### 2. Sentiment Analysis Agent

**Role:** Analyze sentiment from transcript and validate with market news

**Tool:** Tavily Search API

**Capabilities:**
- Extract sentiment from transcript
- Search recent financial news
- Compare transcript vs. market sentiment
- Identify sentiment drivers

**Process:**
```python
1. Extract sentiment from transcript
2. Search Tavily for recent news (5 articles)
3. Analyze market sentiment
4. Compare transcript vs. news sentiment
5. Generate sentiment classification
6. Calculate sentiment score (-1.0 to 1.0)
7. Assess confidence
8. Save sentiment report
```

**Output:** `SentimentAnalysisResult` with classification, score, and validations

**Confidence Threshold:** 65%

---

### 3. Event Detection Agent

**Role:** Identify significant corporate events and verify with official filings

**Tool:** SEC EDGAR Downloader

**Capabilities:**
- Detect events from transcript
- Download SEC filings (8-K, 10-Q, 10-K)
- Verify events against official sources
- Assess event materiality

**Process:**
```python
1. Identify significant events in transcript
2. Download recent SEC filings (8-K, 10-Q)
3. Cross-reference events with filings
4. Verify event details
5. Assess impact (high/medium/low)
6. Determine confidence
7. Save event detection report
```

**Output:** `SignificantEventDetectionResult` with events and validations

**Confidence Threshold:** 70%

---

### 4. Volatility Prediction Agent

**Role:** Predict stock volatility using multi-modal analysis

**Tool:** yfinance API

**Capabilities:**
- Answer structured questions from transcript
- Retrieve historical volatility data
- Analyze price movements
- Integrate sentiment and event data

**Process:**
```python
1. Answer analysis questions from transcript
2. Get historical volatility (1-month) from yfinance
3. Get price movement data
4. Retrieve stock information
5. Integrate sentiment results
6. Integrate event results
7. Predict future volatility
8. Calculate volatility score (0.0 to 1.0)
9. Save volatility report
```

**Output:** `VolatilityPredictionResult` with prediction and validations

**Confidence Threshold:** 60%

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

### Active Guardrails

1. **Confidence Threshold Enforcement**
   - Each agent has minimum confidence requirements
   - Below threshold triggers warnings in reports
   - Ensures quality of outputs

2. **Source Verification Requirement**
   - All findings must cite sources
   - Tool validations tracked and reported
   - Transparency in evidence

3. **Investment Advice Prohibition**
   - Explicitly avoids stock recommendations
   - No buy/sell advice
   - Educational purposes only

4. **Transparent Limitation Disclosure**
   - All reports include disclaimers
   - Limitations clearly stated
   - Confidence levels always shown

### Confidence Thresholds

| Agent | Threshold | Purpose |
|-------|-----------|---------|
| Sentiment Analysis | 65% | Minimum for sentiment claims |
| Event Detection | 70% | Minimum for event verification |
| Volatility Prediction | 60% | Minimum for volatility predictions |

### Operating Boundaries

✗ NO personalized investment advice  
✗ NO stock buy/sell recommendations  
✗ NO guarantees about future performance  
✓ Educational and analytical purposes ONLY  
✓ Must disclose all confidence levels  
✓ Must cite all sources  

### Guardrail Tracking

All guardrail checks are tracked and reported in the final report:

```markdown
## Guardrails Applied

Guardrail Checks Performed: 0

Active Guardrails:
- Confidence threshold enforcement
- Source verification requirement
- Investment advice prohibition
- Transparent limitation disclosure

Operating Boundaries:
- NO personalized investment advice or stock recommendations
- NO guarantees about future stock performance
- All outputs are for educational and analytical purposes only
- Must disclose confidence levels and limitations
```

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
