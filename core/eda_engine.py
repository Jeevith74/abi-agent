import pandas as pd
import numpy as np


class EDAEngine:

    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.numeric_df = df.select_dtypes(include=np.number)

    def summary_statistics(self):
        if self.numeric_df.empty:
            return {}
        return self.numeric_df.describe().to_dict()

    def correlation_matrix(self):
        if self.numeric_df.shape[1] < 2:
            return {}
        return self.numeric_df.corr().to_dict()

    def strong_correlations(self, threshold=0.8):

        if self.numeric_df.shape[1] < 2:
            return []

        corr_matrix = self.numeric_df.corr()
        strong_pairs = set()

        for col1 in corr_matrix.columns:
            for col2 in corr_matrix.columns:

                if col1 >= col2:
                    continue

                corr_value = corr_matrix.loc[col1, col2]

                if abs(corr_value) >= threshold:
                    strong_pairs.add(
                        (col1, col2, float(round(corr_value, 2)))
                    )

        return list(strong_pairs)

    def skewness_detection(self, threshold=1):

        if self.numeric_df.empty:
            return []

        skewness = self.numeric_df.skew()
        return [
            col for col, val in skewness.items()
            if abs(val) > threshold
        ]

    def detect_outliers(self):

        if self.numeric_df.empty:
            return {}

        outlier_summary = {}

        for col in self.numeric_df.columns:

            Q1 = self.numeric_df[col].quantile(0.25)
            Q3 = self.numeric_df[col].quantile(0.75)
            IQR = Q3 - Q1

            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR

            outliers = self.numeric_df[
                (self.numeric_df[col] < lower)
                | (self.numeric_df[col] > upper)
            ]

            outlier_summary[col] = len(outliers)

        return outlier_summary
    def generate_eda_summary(self):

        return {
            "summary_statistics": self.summary_statistics(),
            "strong_correlations": self.strong_correlations(),
            "skewed_columns": self.skewness_detection(),
            "outlier_counts": self.detect_outliers()
        }