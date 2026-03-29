import pandas as pd
from core.schema_detector import SchemaDetector


df = pd.read_csv("data/sample.csv")

detector = SchemaDetector(df)

summary = detector.generate_schema_summary()

print(summary)

#####

from core.eda_engine import EDAEngine

eda = EDAEngine(df)

eda_summary = eda.generate_eda_summary()

print("\nEDA SUMMARY:\n")
print(eda_summary)

####
from agents.insight_agent import InsightAgent

agent = InsightAgent(summary, eda_summary)

print("\nINSIGHTS:\n")
print(agent.generate_insights())

####

from agents.query_agent import QueryAgent

query_agent = QueryAgent(summary, eda_summary)

print("\nQUERY RESPONSE:\n")
print(query_agent.answer_query("Show correlations"))

####

from core.forecasting import ForecastEngine

forecast_engine = ForecastEngine(df, summary)

forecast_summary = forecast_engine.generate_forecast_summary()

print("\nFORECAST SUMMARY:\n")
print(forecast_summary)

####

from core.anomaly_detector import AnomalyDetector

anomaly_detector = AnomalyDetector(df, summary)

print("\nANOMALY SUMMARY:\n")
print(anomaly_detector.generate_anomaly_summary())

####
from agents.summary_agent import SummaryAgent

summary_agent = SummaryAgent(
    summary,
    eda_summary,
    agent.generate_insights(),
    forecast_summary,
    anomaly_detector.generate_anomaly_summary()
)

print("\nEXECUTIVE SUMMARY:\n")
print(summary_agent.generate_summary())