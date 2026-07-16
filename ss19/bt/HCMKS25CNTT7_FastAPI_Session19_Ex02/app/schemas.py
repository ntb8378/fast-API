from typing import Optional, List
from pydantic import BaseModel, ConfigDict


# --- SCHEMAS CHO CLINIC ---
class ClinicCreate(BaseModel):
    clinic_name: str
    specialty: str


# Schema rút gọn của Doctor để lồng vào Clinic Detail
class DoctorInClinicResponse(BaseModel):
    id: int
    doctor_code: str
    salary: float

    model_config = ConfigDict(from_attributes=True)


class ClinicDetailResponse(BaseModel):
    id: int
    clinic_name: str
    specialty: str
    doctors: List[DoctorInClinicResponse] = []

    model_config = ConfigDict(from_attributes=True)


# --- SCHEMAS CHO DOCTOR ---
class DoctorUpdate(BaseModel):
    doctor_code: Optional[str] = None
    salary: Optional[float] = None
    clinic_id: Optional[int] = None


# --- SCHEMAS CHO LICENSE ---
class LicenseResponse(BaseModel):
    id: int
    license_number: str
    issue_by: str
    doctor_id: int

    model_config = ConfigDict(from_attributes=True)
