from ..preprocessing.feature_engineering import build_features


def generate_schema(X_train, preprocessor, feature_metadata: dict) -> dict:
    df_fe = build_features(X_train)
    X_transformed = preprocessor.transform(df_fe)

    encoded_cols = list(X_transformed.columns) if hasattr(X_transformed, "columns") else [
        f"feature_{i}" for i in range(X_transformed.shape[1])
    ]

    dtypes = {}
    for col in df_fe.columns:
        dtype = df_fe[col].dtype
        if dtype == "object":
            dtypes[col] = "category"
        elif dtype in ("int64", "int32"):
            dtypes[col] = "int64"
        elif dtype in ("float64", "float32"):
            dtypes[col] = "float64"
        else:
            dtypes[col] = str(dtype)

    schema = {
        "version": "2.0",
        "n_features_raw": df_fe.shape[1],
        "n_features_encoded": X_transformed.shape[1],
        "feature_names_raw": list(df_fe.columns),
        "feature_names_encoded": encoded_cols,
        "feature_dtypes_raw": dtypes,
        "feature_metadata": feature_metadata,
    }

    return schema
