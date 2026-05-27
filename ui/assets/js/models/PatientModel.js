export class PatientModel {
  constructor(data) {
    this.race = data.race || null;
    this.gender = data.gender;
    this.age = data.age;
    this.admissionTypeId = Number(data.admission_type_id);
    this.dischargeDispositionId = Number(data.discharge_disposition_id);
    this.admissionSourceId = Number(data.admission_source_id);
    this.timeInHospital = Number(data.time_in_hospital);
    this.payerCode = data.payer_code || null;
    this.medicalSpecialty = data.medical_specialty || null;
    this.numLabProcedures = Number(data.num_lab_procedures);
    this.numProcedures = Number(data.num_procedures);
    this.numMedications = Number(data.num_medications);
    this.numberOutpatient = Number(data.number_outpatient);
    this.numberEmergency = Number(data.number_emergency);
    this.numberInpatient = Number(data.number_inpatient);
    this.numberDiagnoses = Number(data.number_diagnoses);
    this.maxGluSerum = data.max_glu_serum || 'None';
    this.a1cResult = data.A1Cresult || 'None';
    this.metformin = data.metformin || 'No';
    this.insulin = data.insulin || 'No';
    this.change = data.change || 'No';
    this.diabetesMed = data.diabetesMed || 'No';
    this.diag1 = data.diag_1 || null;
    this.diag2 = data.diag_2 || null;
    this.diag3 = data.diag_3 || null;
  }

  toRequestDto() {
    return {
      race: this.race,
      gender: this.gender,
      age: this.age,
      admission_type_id: this.admissionTypeId,
      discharge_disposition_id: this.dischargeDispositionId,
      admission_source_id: this.admissionSourceId,
      time_in_hospital: this.timeInHospital,
      payer_code: this.payerCode,
      medical_specialty: this.medicalSpecialty,
      num_lab_procedures: this.numLabProcedures,
      num_procedures: this.numProcedures,
      num_medications: this.numMedications,
      number_outpatient: this.numberOutpatient,
      number_emergency: this.numberEmergency,
      number_inpatient: this.numberInpatient,
      number_diagnoses: this.numberDiagnoses,
      max_glu_serum: this.maxGluSerum,
      A1Cresult: this.a1cResult,
      metformin: this.metformin,
      insulin: this.insulin,
      change: this.change,
      diabetesMed: this.diabetesMed,
      diag_1: this.diag1,
      diag_2: this.diag2,
      diag_3: this.diag3,
    };
  }
}
