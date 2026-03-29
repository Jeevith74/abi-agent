import pandas as pd


class ForecastEngine:

    def __init__(self, df, schema_summary):
        self.df = df
        self.schema = schema_summary

    def detect_time_column(self):

        datetime_cols = self.schema["datetime_columns"]

        if datetime_cols:
            return datetime_cols[0]

        return None

    def detect_target_column(self):

        numeric_cols = self.schema["numeric_columns"]

        if numeric_cols:
            return numeric_cols[-1]

        return None

    def simple_trend_forecast(self):

        time_col = self.detect_time_column()
        target_col = self.detect_target_column()

        if not time_col or not target_col:
            return "No suitable time-series structure detected."

        df_sorted = self.df.sort_values(by=time_col)

        values = df_sorted[target_col].values

        if len(values) < 2:
            return "Not enough data for forecasting."

        trend = values[-1] - values[0]

        if trend > 0:
            direction = "increasing"
        elif trend < 0:
            direction = "decreasing"
        else:
            direction = "stable"

        return f"{target_col} shows an {direction} trend over time."

    def generate_forecast_summary(self):

        return {
            "forecast_result": self.simple_trend_forecast()
        }