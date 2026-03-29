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
    
    def skewness_summary(self):

        skewed_cols = self.eda["skewed_columns"]

        if not skewed_cols:
            return "No significant skewness detected in numeric variables."

        insights = []

        detected_groups = set()

        for col in skewed_cols:

            col_lower = col.lower()

            if "gdp" in col_lower and "gdp" not in detected_groups:
                insights.append(
                    "GDP-related indicators vary widely across observations, reflecting economic scale differences."
                )
                detected_groups.add("gdp")

            elif "inflation" in col_lower and "inflation" not in detected_groups:
                insights.append(
                    "Inflation indicators show strong variation, suggesting macroeconomic instability across regions."
                )
                detected_groups.add("inflation")

            elif "unemployment" in col_lower and "unemployment" not in detected_groups:
                insights.append(
                    "Unemployment rates differ substantially across observations, indicating uneven labor market conditions."
                )
                detected_groups.add("unemployment")

            elif col not in detected_groups:
                insights.append(
                    f"{col} shows a highly skewed distribution and may require transformation before modeling."
                )
                detected_groups.add(col)

        return " ".join(insights)

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
        report.append(self.skewness_summary())  # ← added here

        for insight in self.insights:
                if insight not in report:
                    report.append(insight)

        return " ".join(report)