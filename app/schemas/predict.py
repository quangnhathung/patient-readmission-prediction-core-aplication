from datetime import datetime, timezone
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class Gender(str, Enum):
    male = "Male"
    female = "Female"


class DrugLevel(str, Enum):
    no = "No"
    down = "Down"
    steady = "Steady"
    up = "Up"


class Change(str, Enum):
    no = "No"
    ch = "Ch"


class DiabetesMed(str, Enum):
    no = "No"
    yes = "Yes"


class MaxGluSerum(str, Enum):
    none = "None"
    norm = "Norm"
    gt200 = ">200"
    gt300 = ">300"


class A1CResult(str, Enum):
    none = "None"
    norm = "Norm"
    gt7 = ">7"
    gt8 = ">8"


class PatientData(BaseModel):
    race: Optional[str] = Field(default=None, description="Race of the patient")
    gender: Gender = Field(description="Gender of the patient")
    age: str = Field(description="Age range, e.g. [50-60)", pattern=r'^\[\d+-\d+\)$')
    admission_type_id: int = Field(ge=1, le=8, description="Admission type ID")
    discharge_disposition_id: int = Field(ge=1, le=30, description="Discharge disposition ID")
    admission_source_id: int = Field(ge=1, le=26, description="Admission source ID")
    time_in_hospital: int = Field(ge=1, le=30, description="Days in hospital")
    payer_code: Optional[str] = Field(default=None, description="Insurance payer code")
    medical_specialty: Optional[str] = Field(default=None, description="Medical specialty of attending physician")
    num_lab_procedures: int = Field(ge=0, description="Number of lab procedures")
    num_procedures: int = Field(ge=0, description="Number of procedures")
    num_medications: int = Field(ge=0, description="Number of medications")
    number_outpatient: int = Field(ge=0, description="Number of outpatient visits in past year")
    number_emergency: int = Field(ge=0, description="Number of emergency visits in past year")
    number_inpatient: int = Field(ge=0, description="Number of inpatient visits in past year")
    number_diagnoses: int = Field(ge=0, description="Number of diagnoses")
    max_glu_serum: MaxGluSerum = Field(default=MaxGluSerum.none, description="Max glucose serum test result")
    A1Cresult: A1CResult = Field(default=A1CResult.none, description="A1C test result")
    metformin: DrugLevel = Field(default=DrugLevel.no, description="Metformin dosage change")
    repaglinide: DrugLevel = Field(default=DrugLevel.no)
    nateglinide: DrugLevel = Field(default=DrugLevel.no)
    chlorpropamide: DrugLevel = Field(default=DrugLevel.no)
    glimepiride: DrugLevel = Field(default=DrugLevel.no)
    acetohexamide: DrugLevel = Field(default=DrugLevel.no)
    glipizide: DrugLevel = Field(default=DrugLevel.no)
    glyburide: DrugLevel = Field(default=DrugLevel.no)
    tolbutamide: DrugLevel = Field(default=DrugLevel.no)
    pioglitazone: DrugLevel = Field(default=DrugLevel.no)
    rosiglitazone: DrugLevel = Field(default=DrugLevel.no)
    acarbose: DrugLevel = Field(default=DrugLevel.no)
    miglitol: DrugLevel = Field(default=DrugLevel.no)
    troglitazone: DrugLevel = Field(default=DrugLevel.no)
    tolazamide: DrugLevel = Field(default=DrugLevel.no)
    examide: DrugLevel = Field(default=DrugLevel.no)
    citoglipton: DrugLevel = Field(default=DrugLevel.no)
    insulin: DrugLevel = Field(default=DrugLevel.no)
    glyburide_metformin: DrugLevel = Field(default=DrugLevel.no, alias="glyburide-metformin")
    glipizide_metformin: DrugLevel = Field(default=DrugLevel.no, alias="glipizide-metformin")
    glimepiride_pioglitazone: DrugLevel = Field(default=DrugLevel.no, alias="glimepiride-pioglitazone")
    metformin_rosiglitazone: DrugLevel = Field(default=DrugLevel.no, alias="metformin-rosiglitazone")
    metformin_pioglitazone: DrugLevel = Field(default=DrugLevel.no, alias="metformin-pioglitazone")
    change: Change = Field(default=Change.no, description="Change in diabetes medications")
    diabetesMed: DiabetesMed = Field(default=DiabetesMed.no, description="Diabetes medication prescribed")
    diag_1: Optional[str] = Field(default=None, description="Primary diagnosis (ICD-9 code)")
    diag_2: Optional[str] = Field(default=None, description="Secondary diagnosis (ICD-9 code)")
    diag_3: Optional[str] = Field(default=None, description="Tertiary diagnosis (ICD-9 code)")

    @field_validator("age")
    @classmethod
    def validate_age_range(cls, v: str) -> str:
        valid_ranges = {
            "[0-10)", "[10-20)", "[20-30)", "[30-40)", "[40-50)",
            "[50-60)", "[60-70)", "[70-80)", "[80-90)", "[90-100)",
        }
        if v not in valid_ranges:
            raise ValueError(f"Age must be one of: {', '.join(sorted(valid_ranges))}")
        return v


class SinglePredictionResponse(BaseModel):
    prediction: int = Field(description="Binary prediction: 1 = high risk of readmission within 30 days, 0 = low risk")
    probability: float = Field(description="Probability of readmission within 30 days (0.0 to 1.0)")
    model_name: str = Field(description="Name of the model used for prediction")
    model_version: str = Field(description="Version of the model")
    threshold: float = Field(description="Classification threshold applied")
    timestamp: str = Field(description="ISO-8601 timestamp of prediction")
    status: str = Field(default="success", description="Status of the prediction request")
    processing_time_ms: float = Field(description="Processing time in milliseconds")


class BatchPredictionRequest(BaseModel):
    patients: list[PatientData] = Field(description="List of patients for batch prediction", min_length=1, max_length=1000)


class BatchPredictionResponse(BaseModel):
    predictions: list[SinglePredictionResponse]
    total_count: int
    success_count: int
    model_name: str
    timestamp: str
    status: str = "success"


class PredictionErrorResponse(BaseModel):
    status: str = "error"
    error_code: str
    detail: str
    timestamp: str
