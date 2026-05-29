import pandas as pd
import numpy as np


def load_and_clean_data(
    data_path: str,
    target_col: str = "readmitted",
    positive_class: str = "<30",
    drop_cols: list = None,
    exclude_discharge_ids: list = None,
    keep_first_encounter: bool = True,
) -> pd.DataFrame:
    if drop_cols is None:
        drop_cols = ["encounter_id", "patient_nbr", "weight"]
    if exclude_discharge_ids is None:
        exclude_discharge_ids = [11, 13, 14, 19, 20, 21]

    df = pd.read_csv(data_path, na_values="?", low_memory=False)

    df = df.drop(columns=[c for c in drop_cols if c in df.columns], errors="ignore")

    if "discharge_disposition_id" in df.columns and exclude_discharge_ids:
        before = len(df)
        df = df[~df["discharge_disposition_id"].isin(exclude_discharge_ids)]
        print(f"Removed {before - len(df)} hospice/death encounters")

    if keep_first_encounter and "patient_nbr" in df.columns:
        df = df.sort_values("encounter_id" if "encounter_id" in df.columns else df.index)
        before = len(df)
        df = df.drop_duplicates(subset=["patient_nbr"], keep="first")
        print(f"Kept first encounter: {before} -> {len(df)}")

    y = (df[target_col] == positive_class).astype(int)
    df = df.drop(columns=[target_col])

    return df, y
