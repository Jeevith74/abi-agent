class QueryAgent:

    def __init__(self, schema_summary, eda_summary):
        self.schema = schema_summary
        self.eda = eda_summary

    def answer_correlation_query(self):

        correlations = self.eda["strong_correlations"]

        if not correlations:
            return "No strong correlations detected."

        responses = []

        for col1, col2, value in correlations:
            responses.append(
                f"{col1} and {col2} are strongly correlated ({value})."
            )

        return " ".join(responses)

    def answer_query(self, query):

        query = query.lower()

        if "correlation" in query or "relationship" in query:
            return self.answer_correlation_query()

        return "Query not understood yet."