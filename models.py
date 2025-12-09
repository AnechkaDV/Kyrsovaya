from typing import Optional, List
from datetime import date, time, datetime
from decimal import Decimal
from sqlmodel import SQLModel, Field, Relationship

# --- Справочники ---

class Departments(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    head_doctor_id: Optional[int] = None
    
    doctors: List["Doctors"] = Relationship(back_populates="department")
    cabinets: List["Cabinets"] = Relationship(back_populates="department")

class Specializations(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    
    doctors: List["Doctors"] = Relationship(back_populates="specialization")

class Service_Catalog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    price: Decimal = Field(default=0, decimal_places=2)
    duration_minutes: int

class Diagnoses(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    mkb_code: str
    description: Optional[str] = None

class Appointment_Statuses(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

# --- Структура и Люди ---

class Cabinets(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    number: str
    floor: int
    department_id: Optional[int] = Field(default=None, foreign_key="departments.id")
    
    department: Optional[Departments] = Relationship(back_populates="cabinets")

class Doctors(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    last_name: str
    first_name: str
    middle_name: Optional[str] = None
    specialization_id: Optional[int] = Field(default=None, foreign_key="specializations.id")
    department_id: Optional[int] = Field(default=None, foreign_key="departments.id")
    category: Optional[str] = None
    
    specialization: Optional[Specializations] = Relationship(back_populates="doctors")
    department: Optional[Departments] = Relationship(back_populates="doctors")
    schedules: List["Schedule"] = Relationship(back_populates="doctor")

class Insurance_Policies(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    policy_number: str
    company_name: str
    expiration_date: date
    
    patient: Optional["Patients"] = Relationship(back_populates="policy")

class Patients(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    last_name: str
    first_name: str
    middle_name: Optional[str] = None
    birth_date: date
    phone: Optional[str] = None
    address: Optional[str] = None
    policy_id: Optional[int] = Field(default=None, foreign_key="insurance_policies.id")
    
    policy: Optional[Insurance_Policies] = Relationship(back_populates="patient")
    appointments: List["Appointments"] = Relationship(back_populates="patient")

# --- Процессы ---

class Schedule(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    doctor_id: Optional[int] = Field(default=None, foreign_key="doctors.id")
    cabinet_id: Optional[int] = Field(default=None, foreign_key="cabinets.id")
    day_of_week: int # 1 - Понедельник, 7 - Воскресенье
    start_time: time
    end_time: time
    
    doctor: Optional[Doctors] = Relationship(back_populates="schedules")

class Appointments(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    patient_id: Optional[int] = Field(default=None, foreign_key="patients.id")
    doctor_id: Optional[int] = Field(default=None, foreign_key="doctors.id")
    datetime: datetime
    status_id: Optional[int] = Field(default=None, foreign_key="appointment_statuses.id")
    
    patient: Optional[Patients] = Relationship(back_populates="appointments")
    medical_record: Optional["Medical_Records"] = Relationship(back_populates="appointment")

class Medical_Records(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    appointment_id: int = Field(foreign_key="appointments.id")
    complaints: Optional[str] = None
    anamnesis: Optional[str] = None
    diagnosis_id: Optional[int] = Field(default=None, foreign_key="diagnoses.id")
    recommendations: Optional[str] = None
    
    appointment: Optional[Appointments] = Relationship(back_populates="medical_record")
    prescriptions: List["Prescriptions"] = Relationship(back_populates="medical_record")
    services: List["Services_Rendered"] = Relationship(back_populates="medical_record")

class Prescriptions(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    record_id: Optional[int] = Field(default=None, foreign_key="medical_records.id")
    drug_name: str
    dosage: str
    duration_days: int
    
    medical_record: Optional[Medical_Records] = Relationship(back_populates="prescriptions")

class Services_Rendered(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    record_id: Optional[int] = Field(default=None, foreign_key="medical_records.id")
    service_id: Optional[int] = Field(default=None, foreign_key="service_catalog.id")
    quantity: int = 1
    
    medical_record: Optional[Medical_Records] = Relationship(back_populates="services")
