import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OrdinalEncoder, StandardScaler, MinMaxScaler, FunctionTransformer

from .feature_engineering import build_features


def get_column_types(df: pd.DataFrame) -> dict:
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
    return {"numeric": numeric_cols, "categorical": categorical_cols}


def clip_outliers(df, multiplier=1.5):
    df_clipped = df.copy()
    for col in df_clipped.select_dtypes(include=[np.number]).columns:
        q1 = df_clipped[col].quantile(0.25)
        q3 = df_clipped[col].quantile(0.75)
        iqr = q3 - q1
        lower = q1 - multiplier * iqr
        upper = q3 + multiplier * iqr
        df_clipped[col] = df_clipped[col].clip(lower, upper)
    return df_clipped


def build_preprocessing_pipeline(config: dict):
    numerical_config = config.get("preprocessing", {}).get("numerical", {})
    categorical_config = config.get("preprocessing", {}).get("categorical", {})

    num_impute_strategy = numerical_config.get("strategy", "median")
    scaling = numerical_config.get("scaling")
    clip_outliers_flag = numerical_config.get("clip_outliers", False)

    cat_encoding = categorical_config.get("encoding", "ordinal")
    handle_unknown = categorical_config.get("handle_unknown", "use_encoded_value")
    unknown_value = categorical_config.get("unknown_value", -1)

    cat_fill = config.get("preprocessing", {}).get("missing", {}).get("categorical_fill", "Missing")

    return num_impute_strategy, scaling, clip_outliers_flag, cat_encoding, handle_unknown, unknown_value, cat_fill


def build_preprocessor(X_train, config: dict):
    num_impute_strategy, scaling, clip_outliers_flag, cat_encoding, handle_unknown, unknown_value, cat_fill = (
        build_preprocessing_pipeline(config)
    )

    df_fe = build_features(X_train)
    col_types = get_column_types(df_fe)

    numeric_cols = col_types["numeric"]
    categorical_cols = col_types["categorical"]

    numeric_transformer = []
    if clip_outliers_flag:
        numeric_transformer.append(("clip", FunctionTransformer(clip_outliers, kw_args={"multiplier": 1.5})))
    numeric_transformer.append(("imputer", SimpleImputer(strategy=num_impute_strategy)))
    if scaling == "standard":
        numeric_transformer.append(("scaler", StandardScaler()))
    elif scaling == "minmax":
        numeric_transformer.append(("scaler", MinMaxScaler()))

    categorical_encoder = OrdinalEncoder(
        handle_unknown=handle_unknown,
        unknown_value=unknown_value,
        dtype=np.int32,
    )
    categorical_transformer = Pipeline([
        ("imputer", SimpleImputer(strategy="constant", fill_value=cat_fill)),
        ("encoder", categorical_encoder),
    ])

    transformers = []
    if numeric_cols:
        transformers.append(("num", Pipeline(numeric_transformer), numeric_cols))
    if categorical_cols:
        transformers.append(("cat", categorical_transformer, categorical_cols))

    preprocessor = ColumnTransformer(
        transformers=transformers,
        remainder="drop",
        verbose_feature_names_out=False,
    )

    preprocessor.set_output(transform="pandas")
    preprocessor.fit(df_fe)

    feature_metadata = {
        "numeric_cols": numeric_cols,
        "categorical_cols": categorical_cols,
        "n_features": len(numeric_cols) + len(categorical_cols),
        "n_numeric": len(numeric_cols),
        "n_categorical": len(categorical_cols),
        "encoded_categories": {},
    }

    if categorical_cols:
        cat_encoder = preprocessor.named_transformers_["cat"].named_steps["encoder"]
        for i, col in enumerate(categorical_cols):
            if hasattr(cat_encoder, "categories_") and i < len(cat_encoder.categories_):
                feature_metadata["encoded_categories"][col] = cat_encoder.categories_[i].tolist()

    return preprocessor, feature_metadata, df_fe.columns.tolist()
