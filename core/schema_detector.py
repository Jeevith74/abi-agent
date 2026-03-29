import pandas as pd


class SchemaDetector:

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def dataset_shape(self):
        return {
            "rows": self.df.shape[0],
            "columns": self.df.shape[1]
        }

    def detect_numeric_columns(self):
        return list(self.df.select_dtypes(include=['number']).columns)

    def detect_categorical_columns(self):
        return list(self.df.select_dtypes(include=['object', 'category']).columns)

    def detect_datetime_columns(self):
        datetime_cols = []

        for col in self.df.columns:

            if self.df[col].dtype == "object":

                sample_values = self.df[col].dropna().astype(str).head(5)

                try:
                    parsed_col = pd.to_datetime(
                        sample_values,
                        format="%Y-%m-%d",
                        errors="raise"
                    )

                    datetime_cols.append(col)

                except Exception:
                    continue

        return datetime_cols

        return datetime_cols

    def detect_high_cardinality_columns(self, threshold_ratio=0.9, min_unique=50):

        high_card_cols = []

        for col in self.df.columns:

            unique_count = self.df[col].nunique()
            unique_ratio = unique_count / len(self.df)

            if unique_ratio > threshold_ratio and unique_count > min_unique:
                high_card_cols.append(col)

        return high_card_cols

    def detect_id_columns(self):
        id_cols = []

        for col in self.df.columns:

            if (
            self.df[col].nunique() == len(self.df)
            and "id" in col.lower()
            ):
                id_cols.append(col)

        return id_cols

    def missing_value_summary(self):
        return self.df.isnull().sum().to_dict()

    def column_cardinality(self):
        return {
            col: self.df[col].nunique()
            for col in self.df.columns
        }

    def detect_possible_target_columns(self):
        possible_targets = []

        for col in self.df.columns:
            unique_values = self.df[col].nunique()

            if unique_values < 10:
                possible_targets.append(col)

        return possible_targets

    def generate_schema_summary(self):

        return {
            "shape": self.dataset_shape(),
            "numeric_columns": self.detect_numeric_columns(),
            "categorical_columns": self.detect_categorical_columns(),
            "datetime_columns": self.detect_datetime_columns(),
            "high_cardinality_columns": self.detect_high_cardinality_columns(),
            "id_columns": self.detect_id_columns(),
            "missing_values": self.missing_value_summary(),
            "cardinality": self.column_cardinality(),
            "possible_target_columns": self.detect_possible_target_columns()
        }