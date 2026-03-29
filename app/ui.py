import sys
from pathlib import Path

# Add project root to Python path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

import streamlit as st
import pandas as pd

from core.schema_detector import SchemaDetector
from core.eda_engine import EDAEngine
from agents.insight_agent import InsightAgent
from agents.query_agent import QueryAgent
from core.forecasting import ForecastEngine
from core.anomaly_detector import AnomalyDetector
from agents.summary_agent import SummaryAgent


st.set_page_config(
    page_title="BI Agent",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Global styles ──────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');

    /* ── Reset & base ── */
    html, body, [class*="css"] {
        font-family: 'DM Mono', monospace;
        background-color: #080c10;
        color: #c8d6e5;
    }
    .stApp { background-color: #080c10; }
    .block-container { padding: 2.5rem 3rem 4rem; max-width: 1400px; }

    /* ── Hide Streamlit chrome ── */
    #MainMenu, footer, header { visibility: hidden; }

    /* ── Hero header ── */
    .hero {
        position: relative;
        padding: 3.5rem 0 2.5rem;
        margin-bottom: 3rem;
        border-bottom: 1px solid #1a2535;
        overflow: hidden;
    }
    .hero::before {
        content: '';
        position: absolute;
        top: -80px; left: -60px;
        width: 420px; height: 420px;
        background: radial-gradient(circle, rgba(0,224,168,0.07) 0%, transparent 70%);
        pointer-events: none;
    }
    .hero-eyebrow {
        font-family: 'DM Mono', monospace;
        font-size: 0.68rem;
        letter-spacing: 0.22em;
        color: #00e0a8;
        text-transform: uppercase;
        margin-bottom: 0.6rem;
    }
    .hero-title {
        font-family: 'Syne', sans-serif;
        font-size: 2.8rem;
        font-weight: 800;
        color: #eaf0f8;
        line-height: 1.1;
        margin: 0 0 0.5rem;
        letter-spacing: -0.03em;
    }
    .hero-title span { color: #00e0a8; }
    .hero-subtitle {
        font-size: 0.78rem;
        color: #4a6080;
        letter-spacing: 0.04em;
    }

    /* ── Upload zone ── */
    .upload-zone {
        border: 1px dashed #1e3050;
        border-radius: 10px;
        background: #0b1220;
        padding: 2.2rem 2rem;
        text-align: center;
        transition: border-color 0.2s;
    }
    .upload-zone:hover { border-color: #00e0a8; }

    /* ── Section label ── */
    .section-label {
        font-family: 'DM Mono', monospace;
        font-size: 0.62rem;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        color: #00e0a8;
        margin-bottom: 0.6rem;
    }
    .section-title {
        font-family: 'Syne', sans-serif;
        font-size: 1.15rem;
        font-weight: 700;
        color: #d8e8f5;
        margin-bottom: 1.2rem;
    }

    /* ── Cards ── */
    .card {
        background: #0d1825;
        border: 1px solid #152030;
        border-radius: 10px;
        padding: 1.6rem 1.8rem;
        margin-bottom: 1.2rem;
        position: relative;
    }
    .card::after {
        content: '';
        position: absolute;
        top: 0; left: 0;
        width: 3px; height: 100%;
        background: #00e0a8;
        border-radius: 10px 0 0 10px;
        opacity: 0.7;
    }

    /* ── Pipeline status pills ── */
    .pipeline-bar {
        display: flex;
        gap: 0.5rem;
        flex-wrap: wrap;
        margin-bottom: 2.5rem;
    }
    .pill {
        font-family: 'DM Mono', monospace;
        font-size: 0.62rem;
        letter-spacing: 0.12em;
        padding: 0.3rem 0.75rem;
        border-radius: 20px;
        border: 1px solid #1e3050;
        color: #4a6080;
        background: #0b1220;
        text-transform: uppercase;
    }
    .pill.active {
        border-color: #00e0a8;
        color: #00e0a8;
        background: rgba(0,224,168,0.05);
    }

    /* ── Divider ── */
    .h-rule {
        border: none;
        border-top: 1px solid #111d2b;
        margin: 2rem 0;
    }

    /* ── Streamlit widget overrides ── */
    div[data-testid="stFileUploader"] > label { display: none; }
    div[data-testid="stFileUploader"] section {
        background: #0b1220 !important;
        border: 1px dashed #1e3050 !important;
        border-radius: 10px !important;
    }
    div[data-testid="stDataFrame"] {
        border: 1px solid #152030;
        border-radius: 8px;
        overflow: hidden;
    }
    div[data-testid="stJson"] {
        background: #060a10 !important;
        border: 1px solid #152030;
        border-radius: 8px;
        padding: 1rem !important;
        font-size: 0.78rem;
    }
    .stTextInput > div > div > input {
        background: #0b1220 !important;
        border: 1px solid #1e3050 !important;
        border-radius: 8px !important;
        color: #c8d6e5 !important;
        font-family: 'DM Mono', monospace !important;
        font-size: 0.82rem !important;
        padding: 0.7rem 1rem !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #00e0a8 !important;
        box-shadow: 0 0 0 2px rgba(0,224,168,0.1) !important;
    }
    .stTextInput > label {
        font-family: 'DM Mono', monospace !important;
        font-size: 0.7rem !important;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #4a6080 !important;
    }

    /* ── Response box ── */
    .response-box {
        background: #060a10;
        border: 1px solid #152030;
        border-left: 3px solid #00e0a8;
        border-radius: 8px;
        padding: 1.4rem 1.6rem;
        font-size: 0.84rem;
        line-height: 1.8;
        color: #a8c0d8;
    }

    /* ── Metrics row ── */
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 0.8rem;
        margin-bottom: 1.5rem;
    }
    .metric-tile {
        background: #0b1220;
        border: 1px solid #152030;
        border-radius: 8px;
        padding: 1rem 1.2rem;
    }
    .metric-tile-label {
        font-size: 0.6rem;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        color: #3a5070;
        margin-bottom: 0.3rem;
    }
    .metric-tile-value {
        font-family: 'Syne', sans-serif;
        font-size: 1.4rem;
        font-weight: 700;
        color: #eaf0f8;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="hero">
        <div class="hero-eyebrow">⬡ Autonomous Intelligence</div>
        <h1 class="hero-title">Business <span>Intelligence</span><br>Agent</h1>
        <p class="hero-subtitle">schema · eda · insights · forecasting · anomaly · Q&amp;A</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Upload ─────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-label">01 / Input</div>', unsafe_allow_html=True)
uploaded_file = st.file_uploader("Upload CSV dataset", type=["csv"])

if not uploaded_file:
    st.markdown(
        """
        <div style="text-align:center; padding: 2.5rem; color: #2a4060; font-size:0.76rem; letter-spacing:0.08em;">
            ↑ &nbsp; drop a CSV file to begin analysis
        </div>
        """,
        unsafe_allow_html=True,
    )

# ── Main pipeline ──────────────────────────────────────────────────────────────
if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Pipeline status bar
    st.markdown(
        """
        <div class="pipeline-bar" style="margin-top:1.8rem;">
            <span class="pill active">Schema</span>
            <span class="pill active">EDA</span>
            <span class="pill active">Insights</span>
            <span class="pill active">Forecast</span>
            <span class="pill active">Anomaly</span>
            <span class="pill active">Summary</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Quick stats row ────────────────────────────────────────────────────────
    rows, cols = df.shape
    nulls = int(df.isnull().sum().sum())
    st.markdown(
        f"""
        <div class="metric-grid">
            <div class="metric-tile">
                <div class="metric-tile-label">Rows</div>
                <div class="metric-tile-value">{rows:,}</div>
            </div>
            <div class="metric-tile">
                <div class="metric-tile-label">Columns</div>
                <div class="metric-tile-value">{cols}</div>
            </div>
            <div class="metric-tile">
                <div class="metric-tile-label">Null values</div>
                <div class="metric-tile-value">{nulls:,}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Dataset Preview ────────────────────────────────────────────────────────
    st.markdown('<div class="section-label">02 / Dataset Preview</div>', unsafe_allow_html=True)
    st.dataframe(df.head(), use_container_width=True)

    st.markdown('<hr class="h-rule">', unsafe_allow_html=True)

    # ── Run pipeline ───────────────────────────────────────────────────────────
    with st.spinner("Running analysis pipeline…"):
        schema_detector = SchemaDetector(df)
        schema_summary = schema_detector.generate_schema_summary()

        eda_engine = EDAEngine(df)
        eda_summary = eda_engine.generate_eda_summary()

        insight_agent = InsightAgent(schema_summary, eda_summary)
        insights = insight_agent.generate_insights()

        forecast_engine = ForecastEngine(df, schema_summary)
        forecast_summary = forecast_engine.generate_forecast_summary()

        anomaly_detector = AnomalyDetector(df, schema_summary)
        anomaly_summary = anomaly_detector.generate_anomaly_summary()

        summary_agent = SummaryAgent(
            schema_summary, eda_summary, insights, forecast_summary, anomaly_summary
        )

    # ── Two-column layout for schema + EDA ────────────────────────────────────
    col_l, col_r = st.columns(2, gap="medium")

    with col_l:
        st.markdown('<div class="section-label">03 / Schema Summary</div>', unsafe_allow_html=True)
        st.json(schema_summary)

    with col_r:
        st.markdown('<div class="section-label">04 / EDA Summary</div>', unsafe_allow_html=True)
        st.json(eda_summary)

    st.markdown('<hr class="h-rule">', unsafe_allow_html=True)

    # ── Insights ───────────────────────────────────────────────────────────────
    st.markdown('<div class="section-label">05 / Insights</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="card"><div class="section-title">Key Insights</div>{insights}</div>',
        unsafe_allow_html=True,
    )

    # ── Forecast + Anomaly side-by-side ───────────────────────────────────────
    col_f, col_a = st.columns(2, gap="medium")

    with col_f:
        st.markdown('<div class="section-label">06 / Forecast</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="card">{forecast_summary}</div>',
            unsafe_allow_html=True,
        )

    with col_a:
        st.markdown('<div class="section-label">07 / Anomaly Detection</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="card">{anomaly_summary}</div>',
            unsafe_allow_html=True,
        )

    st.markdown('<hr class="h-rule">', unsafe_allow_html=True)

    # ── Executive Summary ──────────────────────────────────────────────────────
    st.markdown('<div class="section-label">08 / Executive Summary</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="card" style="border-left: 3px solid #00e0a8;">'
        f'<div class="section-title" style="margin-bottom:0.8rem;">Executive Summary</div>'
        f'{summary_agent.generate_summary()}</div>',
        unsafe_allow_html=True,
    )

    st.markdown('<hr class="h-rule">', unsafe_allow_html=True)

    # ── Q&A ────────────────────────────────────────────────────────────────────
    st.markdown('<div class="section-label">09 / Query Interface</div>', unsafe_allow_html=True)
    query = st.text_input("Enter analytics question", placeholder="e.g. Which region has the highest revenue growth?")

    if query:
        with st.spinner("Querying agent…"):
            query_agent = QueryAgent(schema_summary, eda_summary)
            response = query_agent.answer_query(query)

        st.markdown(
            f'<div class="response-box">{response}</div>',
            unsafe_allow_html=True,
        )