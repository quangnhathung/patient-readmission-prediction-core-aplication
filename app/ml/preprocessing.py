from typing import Optional

import numpy as np
import pandas as pd

from app.ml.features import encode_age, feature_engineering


class BasePreprocessor:
    def __init__(self, expected_columns: Optional[list[str]] = None):
        self._expected_columns = expected_columns

    def set_expected_columns(self, columns: list[str]):
        self._expected_columns = columns

    def align_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        if self._expected_columns is None:
            return df
        missing_cols = set(self._expected_columns) - set(df.columns)
        for c in missing_cols:
            df[c] = 0
        extra_cols = set(df.columns) - set(self._expected_columns)
        if extra_cols:
            df = df.drop(columns=list(extra_cols))
        return df[self._expected_columns]


class RandomForestPreprocessor(BasePreprocessor):
    def __init__(self, expected_columns: Optional[list[str]] = None):
        super().__init__(expected_columns)

    def preprocess(self, df: pd.DataFrame) -> pd.DataFrame:
        df_proc = df.copy()

        df_proc["payer_code"] = df_proc["payer_code"].fillna("Missing")
        df_proc["medical_specialty"] = df_proc["medical_specialty"].fillna("Missing")
        df_proc["race"] = df_proc["race"].fillna("Unknown")

        if "age" in df_proc.columns:
            df_proc["age_encoded"] = df_proc["age"].map(encode_age)
            df_proc.drop(columns=["age"], inplace=True)

        obj_cols = df_proc.select_dtypes(include="object").columns.tolist()
        if obj_cols:
            df_proc = pd.get_dummies(df_proc, columns=obj_cols, drop_first=True)

        df_proc = self.align_columns(df_proc)

        numeric_cols = df_proc.select_dtypes(include=[np.number]).columns.tolist()
        df_proc = df_proc[numeric_cols]

        return df_proc


class XGBoostPreprocessor(BasePreprocessor):
    def __init__(self, expected_columns: Optional[list[str]] = None, schema: Optional[dict] = None):
        super().__init__(expected_columns)
        self._schema = schema

    def preprocess(self, df: pd.DataFrame) -> pd.DataFrame:
        df_fe = feature_engineering(df)

        for col in df_fe.select_dtypes(include=["object"]).columns:
            df_fe[col] = df_fe[col].astype("category")

        df_fe = self.align_columns(df_fe)

        if self._schema:
            for col, dtype_str in self._schema.items():
                if col not in df_fe.columns:
                    continue
                if dtype_str == "int64":
                    df_fe[col] = df_fe[col].astype(int)
                elif dtype_str == "float64":
                    df_fe[col] = df_fe[col].astype(float)
                elif dtype_str == "category":
                    df_fe[col] = df_fe[col].astype("category")

        return df_fe
