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