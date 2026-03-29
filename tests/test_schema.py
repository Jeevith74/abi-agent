import pandas as pd
from core.schema_detector import SchemaDetector


df = pd.read_csv("data/sample.csv")

detector = SchemaDetector(df)

summary = detector.generate_schema_summary()

print(summary)