# FinSight Agent - Changelog

## [1.1.0] - 2025-11-03

### Streamlit UI Enhancements

#### Changed
- **Increased processing durations** for more realistic user experience:
  - Sentiment Analysis: 1.5s → 4.0s
  - Event Detection: 1.5s → 5.0s
  - Volatility Prediction: 1.5s → 5.5s
  - Final Report: 1.5s → 3.5s
  - Total processing time: ~18 seconds (up from ~6 seconds)

#### Fixed
- **System Confidence Table**: Fixed rendering issue where table values appeared outside the tab
  - Replaced HTML table with pandas DataFrame for proper rendering
  - Table now displays correctly within the tab container

#### Added
- **Metacognitive Analysis Tab**: Shows coordinator's reasoning and planning
  - User intent interpretation
  - 7-step analysis plan
  - Agents invoked
  - Coordinator confidence with reasoning
  
- **Guardrails & Boundaries Tab**: Displays ethical constraints
  - Guardrail checks performed
  - Active guardrails list
  - Operating boundaries
  - Compliance status
  
- **Tool Validation Audit Data**: All agents now show verification steps
  - Sentiment: Tavily news validation (~6 validations)
  - Events: SEC EDGAR filing verification (~4 validations)
  - Volatility: yfinance market data validation (~4 validations)
  
- **Transcript Insights**: Q&A extracted from earnings call
  - 5 key insights (dividend, revenue, projects, challenges, guidance)
  - Expandable sections with confidence levels
  - Direct quotes from transcript
  
- **Tabbed Interface**: Clear separation of report output vs audit data
  - 📊 Analysis Output tabs for main findings
  - 🔍 Audit Data tabs for verification steps
  - 📝 Transcript Insights tab for earnings call Q&A
  - 🧠 Metacognitive Analysis tab for coordinator reasoning
  - 🛡️ Guardrails tab for ethical constraints

### Documentation

#### Changed
- **Consolidated documentation**: Removed all Streamlit-specific documentation files
  - Deleted: STREAMLIT_README.md, STREAMLIT_FEATURES.md, STREAMLIT_QUICKSTART.md
  - Deleted: DEMO_GUIDE.md
  - Deleted: Technical implementation docs (BEFORE_AFTER_COMPARISON.md, FIXES_SUMMARY.md, etc.)

- **Updated README.md**: Streamlined with essential information only
  - Simplified Streamlit section to core functionality
  - Removed verbose feature descriptions
  - Kept only practical usage information

#### Added
- **CHANGELOG.md**: Version history and changes tracking

### Dependencies

#### Added
- `pandas>=2.0.0` - Required for DataFrame table rendering in Streamlit

### Technical Details

#### Files Modified
- `app.py`: Updated processing times and display functions (~200 lines)
- `api.py`: Enhanced data parsing for audit information (~120 lines)
- `requirements.txt`: Added pandas dependency
- `README.md`: Updated Streamlit section and project structure

#### Data Coverage
- Increased from 20% to 100% of available data visible in UI
- All tool validations now exposed to users
- Complete audit trail for all agent decisions

---

## [1.0.0] - 2025-11-02

### Initial Release

#### Core Features
- Multi-agent orchestration with LangGraph
- 4 specialized agents (Coordinator, Sentiment, Events, Volatility)
- External tool integration (Tavily, SEC EDGAR, yfinance)
- Metacognitive reasoning system
- Individual markdown reports per agent
- Comprehensive final report
- CLI interface
- Programmatic API

#### Streamlit UI
- File upload for earnings calls
- Real-time progress indicators
- Sequential display of results
- Professional gradient styling
- Confidence badges and metrics
- Status indicators

#### Guardrails
- Confidence threshold enforcement
- Source verification requirements
- Investment advice prohibition
- Transparent limitation disclosure

#### Documentation
- Comprehensive README
- Setup and configuration guides
- Usage examples
- Architecture diagrams
- API documentation

---

## Version History

| Version | Date | Description |
|---------|------|-------------|
| 1.1.0 | 2025-11-03 | UI enhancements, audit data integration, documentation consolidation |
| 1.0.0 | 2025-11-02 | Initial release with core functionality |

---

## Upgrade Guide

### From 1.0.0 to 1.1.0

**Required Changes:**
1. Update dependencies:
   ```bash
   pip install -r requirements.txt
   ```

**Optional Changes:**
- None - fully backward compatible

**Breaking Changes:**
- None

**New Features Available:**
- Audit data tabs in Streamlit UI
- Metacognitive analysis visibility
- Transcript insights display
- Enhanced transparency features

---

**Maintained by:** FinSight Agent Team  
**License:** Apache 2.0

