import numpy as np
import pandas as pd


def map_icd9_category(val) -> str:
    if pd.isna(val) or str(val).strip() in ("?", "None", ""):
        return "Missing"
    val_str = str(val).strip().upper()
    if val_str.startswith("V"):
        return "Supplementary"
    if val_str.startswith("E"):
        return "ExternalCause"
    try:
        v = float(val_str)
        if np.floor(v) == 250:
            return "Diabetes"
        if 390 <= v <= 459 or v == 785:
            return "Circulatory"
        if 460 <= v <= 519 or v == 786:
            return "Respiratory"
        if 520 <= v <= 579 or v == 787:
            return "Digestive"
        if 800 <= v <= 999:
            return "Injury"
        if 710 <= v <= 739:
            return "Musculoskeletal"
        if 580 <= v <= 629 or v == 788:
            return "Genitourinary"
        if 140 <= v <= 239:
            return "Neoplasm"
        if 290 <= v <= 319:
            return "Mental"
    except ValueError:
        pass
    return "Other"


def encode_discharge_disposition(val) -> str:
    if pd.isna(val):
        return "Unknown"
    v = int(val)
    if v in (11, 19, 20, 21):
        return "Hospice_Expired"
    if v in (13, 14):
        return "AMA"
    if v in (2, 3, 4, 5, 6, 8, 9, 10, 12, 15, 16, 17, 22, 23, 24, 27, 28, 29, 30):
        return "Transfer_SNF"
    if v in (1, 7):
        return "Home"
    return "Other"


def encode_admission_type(val) -> str:
    if pd.isna(val):
        return "Unknown"
    mapping = {1: "Emergency", 2: "Urgent", 3: "Elective", 4: "Newborn", 5: "Not_Available", 6: "NULL", 7: "Trauma", 8: "Not_Mapped"}
    return mapping.get(int(val), "Other")


def encode_admission_source(val) -> str:
    if pd.isna(val):
        return "Unknown"
    v = int(val)
    if v in (1, 2, 3):
        return "Physician_Referral"
    if v in (4, 5, 6, 10, 22, 25, 26):
        return "Transfer_Hospital"
    if v == 7:
        return "Emergency_Room"
    if v in (8, 9):
        return "Court_Law"
    return "Other"


def encode_age(val) -> int:
    age_map = {
        "[0-10)": 5, "[10-20)": 15, "[20-30)": 25, "[30-40)": 35,
        "[40-50)": 45, "[50-60)": 55, "[60-70)": 65, "[70-80)": 75,
        "[80-90)": 85, "[90-100)": 95,
    }
    return age_map.get(str(val), 55)


DRUG_COLS = [
    "metformin", "repaglinide", "nateglinide", "chlorpropamide",
    "glimepiride", "acetohexamide", "glipizide", "glyburide",
    "tolbutamide", "pioglitazone", "rosiglitazone", "acarbose",
    "miglitol", "troglitazone", "tolazamide", "examide",
    "citoglipton", "insulin",
    "glyburide-metformin", "glipizide-metformin",
    "glimepiride-pioglitazone", "metformin-rosiglitazone",
    "metformin-pioglitazone",
]

def feature_engineering(df: pd.DataFrame) -> pd.DataFrame:
    df_fe = df.copy()

    if "age" in df_fe.columns:
        df_fe["age_numeric"] = df_fe["age"].apply(encode_age)
        df_fe.drop(columns=["age"], inplace=True)
    if "discharge_disposition_id" in df_fe.columns:
        df_fe["discharge_risk_group"] = df_fe["discharge_disposition_id"].apply(encode_discharge_disposition)
        df_fe.drop(columns=["discharge_disposition_id"], inplace=True)
    if "admission_type_id" in df_fe.columns:
        df_fe["admission_type_group"] = df_fe["admission_type_id"].apply(encode_admission_type)
        df_fe.drop(columns=["admission_type_id"], inplace=True)
    if "admission_source_id" in df_fe.columns:
        df_fe["admission_source_group"] = df_fe["admission_source_id"].apply(encode_admission_source)
        df_fe.drop(columns=["admission_source_id"], inplace=True)

    for col in ["diag_1", "diag_2", "diag_3"]:
        if col in df_fe.columns:
            df_fe[f"{col}_grouped"] = df_fe[col].apply(map_icd9_category)
            df_fe.drop(columns=[col], inplace=True)

    df_fe["total_past_visits"] = (
        df_fe.get("number_outpatient", 0)
        + df_fe.get("number_emergency", 0)
        + df_fe.get("number_inpatient", 0)
    )
    if "number_inpatient" in df_fe.columns:
        df_fe["log_inpatient"] = np.log1p(df_fe["number_inpatient"])

    df_fe["treatment_complexity"] = (
        df_fe.get("time_in_hospital", 0)
        * np.log1p(df_fe.get("num_medications", 1))
    )
    df_fe["lab_to_days_ratio"] = df_fe.get("num_lab_procedures", 0) / (
        df_fe.get("time_in_hospital", 1) + 1
    )

    existing_meds = [c for c in DRUG_COLS if c in df_fe.columns]
    if existing_meds:
        df_fe["num_med_changes"] = df_fe[existing_meds].apply(
            lambda row: sum((row == "Up") | (row == "Down")), axis=1
        )
        df_fe["num_active_meds"] = df_fe[existing_meds].apply(
            lambda row: sum(row != "No"), axis=1
        )

    if "insulin" in df_fe.columns:
        df_fe["insulin_used"] = (df_fe["insulin"] != "No").astype(int)
        df_fe["insulin_changed"] = df_fe["insulin"].isin(["Up", "Down"]).astype(int)

    if "A1Cresult" in df_fe.columns:
        df_fe["A1C_abnormal"] = df_fe["A1Cresult"].isin([">7", ">8"]).astype(int)
        df_fe["A1C_tested"] = (df_fe["A1Cresult"] != "None").astype(int)
    if "max_glu_serum" in df_fe.columns:
        df_fe["glu_abnormal"] = df_fe["max_glu_serum"].isin([">200", ">300"]).astype(int)
        df_fe["glu_tested"] = (df_fe["max_glu_serum"] != "None").astype(int)

    if "diag_1_grouped" in df_fe.columns:
        df_fe["primary_diag_is_diabetes"] = (df_fe["diag_1_grouped"] == "Diabetes").astype(int)

    df_fe["composite_risk"] = (
        df_fe.get("log_inpatient", 0) * 3.0
        + df_fe.get("time_in_hospital", 0) * 0.5
        + df_fe.get("num_med_changes", 0) * 1.5
        + df_fe.get("number_emergency", 0) * 2.0
        + df_fe.get("A1C_abnormal", 0) * 1.0
    )

    return df_fe
