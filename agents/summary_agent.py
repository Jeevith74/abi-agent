class SummaryAgent:

    def __init__(self, schema_summary, eda_summary, insights, forecast_summary, anomaly_summary):
        self.schema = schema_summary
        self.eda = eda_summary
        self.insights = insights
        self.forecast = forecast_summary
        self.anomalies = anomaly_summary

    def dataset_overview(self):

        rows = self.schema["shape"]["rows"]
        cols = self.schema["shape"]["columns"]

        return f"The dataset contains {rows} rows and {cols} columns."

    def correlation_summary(self):

        correlations = self.eda["strong_correlations"]

        if not correlations:
            return "No strong correlations detected between numeric variables."

        col1, col2, value = correlations[0]

        return (
            f"A strong correlation exists between {col1} and {col2} ({value}), "
            "suggesting these variables move together."
        )

    def anomaly_summary(self):

        if isinstance(self.anomalies, list):
            return self.anomalies[0]

        return "No anomaly information available."

    def forecast_summary_text(self):

        return self.forecast.get(
            "forecast_result",
            "No forecasting insight available."
        )

    def generate_summary(self):

        report = []

        report.append(self.dataset_overview())
        report.append(self.correlation_summary())
        report.append(self.forecast_summary_text())
        report.append(self.anomaly_summary())

        if self.insights:
            report.extend(self.insights)

        return " ".join(report)