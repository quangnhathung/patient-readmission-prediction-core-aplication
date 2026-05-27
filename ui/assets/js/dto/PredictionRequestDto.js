export class PredictionRequestDto {
  constructor(data) {
    this.race = data.race || null;
    this.gender = data.gender;
    this.age = data.age;
    this.admission_type_id = Number(data.admission_type_id);
    this.discharge_disposition_id = Number(data.discharge_disposition_id);
    this.admission_source_id = Number(data.admission_source_id);
    this.time_in_hospital = Number(data.time_in_hospital);
    this.payer_code = data.payer_code || null;
    this.medical_specialty = data.medical_specialty || null;
    this.num_lab_procedures = Number(data.num_lab_procedures);
    this.num_procedures = Number(data.num_procedures);
    this.num_medications = Number(data.num_medications);
    this.number_outpatient = Number(data.number_outpatient);
    this.number_emergency = Number(data.number_emergency);
    this.number_inpatient = Number(data.number_inpatient);
    this.number_diagnoses = Number(data.number_diagnoses);
    this.max_glu_serum = data.max_glu_serum || 'None';
    this.A1Cresult = data.A1Cresult || 'None';
    this.metformin = data.metformin || 'No';
    this.repaglinide = 'No';
    this.nateglinide = 'No';
    this.chlorpropamide = 'No';
    this.glimepiride = 'No';
    this.acetohexamide = 'No';
    this.glipizide = 'No';
    this.glyburide = 'No';
    this.tolbutamide = 'No';
    this.pioglitazone = 'No';
    this.rosiglitazone = 'No';
    this.acarbose = 'No';
    this.miglitol = 'No';
    this.troglitazone = 'No';
    this.tolazamide = 'No';
    this.examide = 'No';
    this.citoglipton = 'No';
    this.insulin = data.insulin || 'No';
    this['glyburide-metformin'] = 'No';
    this['glipizide-metformin'] = 'No';
    this['glimepiride-pioglitazone'] = 'No';
    this['metformin-rosiglitazone'] = 'No';
    this['metformin-pioglitazone'] = 'No';
    this.change = data.change || 'No';
    this.diabetesMed = data.diabetesMed || 'No';
    this.diag_1 = data.diag_1 || null;
    this.diag_2 = data.diag_2 || null;
    this.diag_3 = data.diag_3 || null;
  }

  toJSON() {
    return {
      race: this.race,
      gender: this.gender,
      age: this.age,
      admission_type_id: this.admission_type_id,
      discharge_disposition_id: this.discharge_disposition_id,
      admission_source_id: this.admission_source_id,
      time_in_hospital: this.time_in_hospital,
      payer_code: this.payer_code,
      medical_specialty: this.medical_specialty,
      num_lab_procedures: this.num_lab_procedures,
      num_procedures: this.num_procedures,
      num_medications: this.num_medications,
      number_outpatient: this.number_outpatient,
      number_emergency: this.number_emergency,
      number_inpatient: this.number_inpatient,
      number_diagnoses: this.number_diagnoses,
      max_glu_serum: this.max_glu_serum,
      A1Cresult: this.A1Cresult,
      metformin: this.metformin,
      repaglinide: this.repaglinide,
      nateglinide: this.nateglinide,
      chlorpropamide: this.chlorpropamide,
      glimepiride: this.glimepiride,
      acetohexamide: this.acetohexamide,
      glipizide: this.glipizide,
      glyburide: this.glyburide,
      tolbutamide: this.tolbutamide,
      pioglitazone: this.pioglitazone,
      rosiglitazone: this.rosiglitazone,
      acarbose: this.acarbose,
      miglitol: this.miglitol,
      troglitazone: this.troglitazone,
      tolazamide: this.tolazamide,
      examide: this.examide,
      citoglipton: this.citoglipton,
      insulin: this.insulin,
      'glyburide-metformin': this['glyburide-metformin'],
      'glipizide-metformin': this['glipizide-metformin'],
      'glimepiride-pioglitazone': this['glimepiride-pioglitazone'],
      'metformin-rosiglitazone': this['metformin-rosiglitazone'],
      'metformin-pioglitazone': this['metformin-pioglitazone'],
      change: this.change,
      diabetesMed: this.diabetesMed,
      diag_1: this.diag_1,
      diag_2: this.diag_2,
      diag_3: this.diag_3,
    };
  }
}
