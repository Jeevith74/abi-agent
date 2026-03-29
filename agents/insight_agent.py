class InsightAgent:

    def __init__(self, schema_summary, eda_summary):
        self.schema = schema_summary
        self.eda = eda_summary

    def correlation_insights(self):

        insights = []

        for col1, col2, value in self.eda["strong_correlations"]:

            insights.append(
                f"{col1} and {col2} show strong correlation ({value}), "
                "suggesting a potential relationship between these variables."
            )

        return insights

    def skewness_insights(self):

        insights = []

        for col in self.eda["skewed_columns"]:

            insights.append(
                f"{col} is highly skewed, which may impact statistical modeling accuracy."
            )

        return insights

    def outlier_insights(self):

        insights = []

        for col, count in self.eda["outlier_counts"].items():

            if count > 0:
                insights.append(
                    f"{count} potential outliers detected in column '{col}'."
                )

        return insights

    def generate_insights(self):

        insights = []

        insights.extend(self.correlation_insights())
        insights.extend(self.skewness_insights())
        insights.extend(self.outlier_insights())

        return insights
    