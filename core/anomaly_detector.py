import numpy as np


class AnomalyDetector:

    def __init__(self, df, schema_summary):
        self.df = df
        self.schema = schema_summary
        self.numeric_cols = schema_summary["numeric_columns"]

    def zscore_detection(self, threshold=3):

        anomalies = {}

        for col in self.numeric_cols:

            values = self.df[col]

            if len(values) < 2:
                continue

            mean = values.mean()
            std = values.std()

            if std == 0:
                anomalies[col] = 0
                continue

            zscores = (values - mean) / std

            anomaly_count = np.sum(np.abs(zscores) > threshold)

            anomalies[col] = int(anomaly_count)

        return anomalies

    def generate_anomaly_summary(self):

        anomaly_counts = self.zscore_detection()

        results = []

        for col, count in anomaly_counts.items():

            if count > 0:
                results.append(
                    f"{col} contains {count} anomalous values."
                )

        if not results:
            return ["No significant anomalies detected."]

        return results