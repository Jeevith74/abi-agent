# Autonomous Business Intelligence Copilot

> A modular analytics assistant that automatically interprets tabular datasets and generates structured analytical insights — no manual configuration required.

ABI Copilot performs schema inference, statistical profiling, anomaly detection, trend detection, correlation analysis, natural-language query handling, and executive summary generation directly from raw CSV inputs.

---

## Overview

After uploading a dataset, ABI Copilot automatically:

- Infers dataset schema and column types
- Identifies numeric, categorical, and datetime columns
- Detects correlations between variables
- Flags skewed distributions and outliers
- Detects anomalous observations
- Determines trend direction when time structure exists
- Generates natural-language statistical insights
- Answers structured analytics questions
- Produces an executive summary of the dataset

The system is designed as a modular pipeline where each component can be extended independently.

---

## Architecture

```
Dataset
  → Schema Detection
  → Statistical Profiling (EDA Engine)
  → Insight Generation
  → Query Interpretation
  → Trend Detection
  → Anomaly Detection
  → Executive Summary Generation
  → Streamlit Interface
```

Each stage operates as an independent module with no hard dependencies on other stages.

---

## Features

### Schema Detection
Automatically identifies column types and dataset structure:
- Numeric, categorical, datetime, and identifier columns
- Missing values and null rates
- Column cardinality
- Candidate target variables

### Statistical Profiling Engine
Performs automated statistical analysis:
- Correlation detection between numeric variables
- Skewness and distribution inspection
- Outlier detection across columns

### Insight Generation
Transforms statistical signals into plain-language statements. Example:

> *Sales and profit show strong correlation (0.98), suggesting profitability scales with revenue.*

### Natural Language Query Interface
Supports structured analytics questions such as:
- `Show correlations`
- `Are there anomalies?`
- `Is profit increasing?`
- `Which variables are related?`
- `Explain dataset insights`

### Trend Detection
Detects time-series structure automatically and reports trend direction. Example:

> *Profit shows an increasing trend over time.*

### Anomaly Detection
Identifies unusual observations across numeric variables using statistical deviation methods.

### Executive Summary Generation
Produces a structured dataset-level report covering:
- Dataset overview
- Strongest variable relationships
- Anomaly signals
- Distribution imbalance indicators
- Trend interpretation

### Interactive Interface
Streamlit UI supports:
- Dataset upload and preview
- KPI overview (rows, columns, null counts)
- Structured analytics panels
- Executive summary panel
- Natural language query interaction

---

## Project Structure

```
abi-agent/
│
├── agents/
│   ├── insight_agent.py       # Converts statistical signals to language
│   ├── query_agent.py         # Handles natural language analytics queries
│   └── summary_agent.py       # Generates executive dataset summaries
│
├── core/
│   ├── schema_detector.py     # Infers column types and dataset structure
│   ├── eda_engine.py          # Statistical profiling and correlation analysis
│   ├── forecasting.py         # Trend detection engine
│   └── anomaly_detector.py    # Anomaly detection across numeric variables
│
├── app/
│   └── ui.py                  # Streamlit interface
│
├── tests/
│   └── test_schema.py
│
├── requirements.txt
└── README.md
```

---

## Installation

**Clone the repository:**

```bash
git clone https://github.com/Jeevith74/abi-agent
cd abi-agent
```

**Create a virtual environment:**

```bash
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS / Linux
```

**Install dependencies:**

```bash
pip install -r requirements.txt
```

---

## Running the Application

```bash
streamlit run app/ui.py
```

Upload any CSV dataset via the file uploader to begin analysis. The pipeline runs automatically — schema detection, EDA, insights, forecasting, and anomaly detection execute in sequence.

---

## Example Queries

Questions supported by the natural language query interface:

| Query | What it does |
|---|---|
| `Show correlations` | Lists strongest variable relationships |
| `Are there anomalies?` | Flags statistically unusual observations |
| `Which variables are related?` | Identifies correlated feature pairs |
| `Is profit increasing?` | Runs trend detection on the target variable |
| `Explain dataset insights` | Returns the full insight summary |

---

## Example Datasets for Testing

These datasets are recommended for demonstrating the full pipeline:

| Dataset | What it demonstrates |
|---|---|
| Superstore Sales | Correlation detection, distribution analysis |
| Walmart Sales Forecasting | Trend detection, seasonality |
| World Bank Indicators | Multi-variable correlation, anomalies |
| Airline Passenger Dataset | Time-series trend reasoning |
| Manufacturing Production | Outlier and skewness detection |

---

## Motivation

Most dashboards visualize metrics but do not interpret them.

ABI Copilot demonstrates how automated statistical reasoning layers can convert raw datasets into structured analytical summaries without manual feature engineering or notebook-based workflows. The architecture reflects the reasoning pipeline used by modern analytics assistants — schema-aware, modular, and composable.

---

## Future Extensions

Planned improvements:

- Semantic column-aware query understanding
- LLM-based natural language explanation layer
- Feature importance ranking
- SQL database connectors
- Multi-dataset comparison support
- Vector-based metadata retrieval

---

## License

MIT — see `LICENSE` for details.
