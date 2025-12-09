from fastapi import FastAPI, HTTPException, Depends, Query
from sqlmodel import SQLModel, Session, create_engine, select
from typing import List, Optional
from datetime import date, time, datetime
from decimal import Decimal
from fastapi.middleware.cors import CORSMiddleware

from models import (
    Departments, Specializations, Cabinets, Service_Catalog, Diagnoses, Appointment_Statuses,
    Doctors, Insurance_Policies, Patients, Schedule, Appointments, Medical_Records,
    Prescriptions, Services_Rendered
)


DATABASE_URL = "postgresql://postgres:puee2OSOJYZxFAaM@localhost/polyclinic_db"
engine = create_engine(DATABASE_URL)

# --- ИНИЦИАЛИЗАЦИЯ ПРИЛОЖЕНИЯ ---
app = FastAPI(
    title="Polyclinic Full API",
    description="Полное API для управления поликлиникой (14 таблиц, CRUD).",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Зависимость для получения сессии БД
def get_session():
    with Session(engine) as session:
        yield session

# --- СОБЫТИЯ ПРИ ЗАПУСКЕ ---
@app.on_event("startup")
def on_startup():
    # Создаем таблицы, если их нет. Данные НЕ добавляются.
    SQLModel.metadata.create_all(engine)

@app.get("/")
def root():
    return {"message": "API Поликлиники готово. Перейдите на /docs для просмотра документации."}

# ===================================================================================
# --- МОДЕЛИ ДЛЯ ОБНОВЛЕНИЯ (UPDATE MODELS) ---
# ===================================================================================
# Определяем схемы Pydantic, где все поля необязательны, для метода PATCH

class DepartmentsUpdate(SQLModel):
    name: Optional[str] = None
    head_doctor_id: Optional[int] = None

class SpecializationsUpdate(SQLModel):
    name: Optional[str] = None

class CabinetsUpdate(SQLModel):
    number: Optional[str] = None
    floor: Optional[int] = None
    department_id: Optional[int] = None

class Service_CatalogUpdate(SQLModel):
    name: Optional[str] = None
    price: Optional[Decimal] = None
    duration_minutes: Optional[int] = None

class DiagnosesUpdate(SQLModel):
    mkb_code: Optional[str] = None
    description: Optional[str] = None

class Appointment_StatusesUpdate(SQLModel):
    name: Optional[str] = None

class DoctorsUpdate(SQLModel):
    last_name: Optional[str] = None
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    specialization_id: Optional[int] = None
    department_id: Optional[int] = None
    category: Optional[str] = None

class Insurance_PoliciesUpdate(SQLModel):
    policy_number: Optional[str] = None
    company_name: Optional[str] = None
    expiration_date: Optional[date] = None

class PatientsUpdate(SQLModel):
    last_name: Optional[str] = None
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    birth_date: Optional[date] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    policy_id: Optional[int] = None

class ScheduleUpdate(SQLModel):
    doctor_id: Optional[int] = None
    cabinet_id: Optional[int] = None
    day_of_week: Optional[int] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None

class AppointmentsUpdate(SQLModel):
    patient_id: Optional[int] = None
    doctor_id: Optional[int] = None
    datetime: Optional[str] = None
    status_id: Optional[int] = None

class Medical_RecordsUpdate(SQLModel):
    appointment_id: Optional[int] = None
    complaints: Optional[str] = None
    anamnesis: Optional[str] = None
    diagnosis_id: Optional[int] = None
    recommendations: Optional[str] = None

class PrescriptionsUpdate(SQLModel):
    record_id: Optional[int] = None
    drug_name: Optional[str] = None
    dosage: Optional[str] = None
    duration_days: Optional[int] = None

class Services_RenderedUpdate(SQLModel):
    record_id: Optional[int] = None
    service_id: Optional[int] = None
    quantity: Optional[int] = None


# ===================================================================================
# --- CRUD ОПЕРАЦИИ (ДЛЯ ВСЕХ 14 ТАБЛИЦ) ---
# ===================================================================================

# 1. Departments
@app.post("/departments/", response_model=Departments, tags=["Departments"])
def create_department(item: Departments, session: Session = Depends(get_session)):
    session.add(item)
    session.commit()
    session.refresh(item)
    return item

@app.get("/departments/", response_model=List[Departments], tags=["Departments"])
def read_departments(session: Session = Depends(get_session)):
    return session.exec(select(Departments)).all()

@app.get("/departments/{item_id}", response_model=Departments, tags=["Departments"])
def read_department(item_id: int, session: Session = Depends(get_session)):
    item = session.get(Departments, item_id)
    if not item: raise HTTPException(status_code=404, detail="Not found")
    return item

@app.patch("/departments/{item_id}", response_model=Departments, tags=["Departments"])
def update_department(item_id: int, update_data: DepartmentsUpdate, session: Session = Depends(get_session)):
    item = session.get(Departments, item_id)
    if not item: raise HTTPException(status_code=404, detail="Not found")
    data = update_data.model_dump(exclude_unset=True)
    for key, value in data.items(): setattr(item, key, value)
    session.add(item); session.commit(); session.refresh(item)
    return item

@app.delete("/departments/{item_id}", tags=["Departments"])
def delete_department(item_id: int, session: Session = Depends(get_session)):
    item = session.get(Departments, item_id)
    if not item: raise HTTPException(status_code=404, detail="Not found")
    session.delete(item); session.commit()
    return {"ok": True}


# 2. Specializations
@app.post("/specializations/", response_model=Specializations, tags=["Specializations"])
def create_specialization(item: Specializations, session: Session = Depends(get_session)):
    session.add(item); session.commit(); session.refresh(item)
    return item

@app.get("/specializations/", response_model=List[Specializations], tags=["Specializations"])
def read_specializations(session: Session = Depends(get_session)):
    return session.exec(select(Specializations)).all()

@app.get("/specializations/{item_id}", response_model=Specializations, tags=["Specializations"])
def read_specialization(item_id: int, session: Session = Depends(get_session)):
    item = session.get(Specializations, item_id)
    if not item: raise HTTPException(status_code=404, detail="Not found")
    return item

@app.patch("/specializations/{item_id}", response_model=Specializations, tags=["Specializations"])
def update_specialization(item_id: int, update_data: SpecializationsUpdate, session: Session = Depends(get_session)):
    item = session.get(Specializations, item_id)
    if not item: raise HTTPException(status_code=404, detail="Not found")
    data = update_data.model_dump(exclude_unset=True)
    for key, value in data.items(): setattr(item, key, value)
    session.add(item); session.commit(); session.refresh(item)
    return item

@app.delete("/specializations/{item_id}", tags=["Specializations"])
def delete_specialization(item_id: int, session: Session = Depends(get_session)):
    item = session.get(Specializations, item_id)
    if not item: raise HTTPException(status_code=404, detail="Not found")
    session.delete(item); session.commit()
    return {"ok": True}


# 3. Cabinets
@app.post("/cabinets/", response_model=Cabinets, tags=["Cabinets"])
def create_cabinet(item: Cabinets, session: Session = Depends(get_session)):
    session.add(item); session.commit(); session.refresh(item)
    return item

@app.get("/cabinets/", response_model=List[Cabinets], tags=["Cabinets"])
def read_cabinets(session: Session = Depends(get_session)):
    return session.exec(select(Cabinets)).all()

@app.get("/cabinets/{item_id}", response_model=Cabinets, tags=["Cabinets"])
def read_cabinet(item_id: int, session: Session = Depends(get_session)):
    item = session.get(Cabinets, item_id)
    if not item: raise HTTPException(status_code=404, detail="Not found")
    return item

@app.patch("/cabinets/{item_id}", response_model=Cabinets, tags=["Cabinets"])
def update_cabinet(item_id: int, update_data: CabinetsUpdate, session: Session = Depends(get_session)):
    item = session.get(Cabinets, item_id)
    if not item: raise HTTPException(status_code=404, detail="Not found")
    data = update_data.model_dump(exclude_unset=True)
    for key, value in data.items(): setattr(item, key, value)
    session.add(item); session.commit(); session.refresh(item)
    return item

@app.delete("/cabinets/{item_id}", tags=["Cabinets"])
def delete_cabinet(item_id: int, session: Session = Depends(get_session)):
    item = session.get(Cabinets, item_id)
    if not item: raise HTTPException(status_code=404, detail="Not found")
    session.delete(item); session.commit()
    return {"ok": True}


# 4. Service_Catalog
@app.post("/services/", response_model=Service_Catalog, tags=["Service Catalog"])
def create_service(item: Service_Catalog, session: Session = Depends(get_session)):
    session.add(item); session.commit(); session.refresh(item)
    return item

@app.get("/services/", response_model=List[Service_Catalog], tags=["Service Catalog"])
def read_services(session: Session = Depends(get_session)):
    return session.exec(select(Service_Catalog)).all()

@app.get("/services/{item_id}", response_model=Service_Catalog, tags=["Service Catalog"])
def read_service(item_id: int, session: Session = Depends(get_session)):
    item = session.get(Service_Catalog, item_id)
    if not item: raise HTTPException(status_code=404, detail="Not found")
    return item

@app.patch("/services/{item_id}", response_model=Service_Catalog, tags=["Service Catalog"])
def update_service(item_id: int, update_data: Service_CatalogUpdate, session: Session = Depends(get_session)):
    item = session.get(Service_Catalog, item_id)
    if not item: raise HTTPException(status_code=404, detail="Not found")
    data = update_data.model_dump(exclude_unset=True)
    for key, value in data.items(): setattr(item, key, value)
    session.add(item); session.commit(); session.refresh(item)
    return item

@app.delete("/services/{item_id}", tags=["Service Catalog"])
def delete_service(item_id: int, session: Session = Depends(get_session)):
    item = session.get(Service_Catalog, item_id)
    if not item: raise HTTPException(status_code=404, detail="Not found")
    session.delete(item); session.commit()
    return {"ok": True}


# 5. Diagnoses
@app.post("/diagnoses/", response_model=Diagnoses, tags=["Diagnoses"])
def create_diagnosis(item: Diagnoses, session: Session = Depends(get_session)):
    session.add(item); session.commit(); session.refresh(item)
    return item

@app.get("/diagnoses/", response_model=List[Diagnoses], tags=["Diagnoses"])
def read_diagnoses(session: Session = Depends(get_session)):
    return session.exec(select(Diagnoses)).all()

@app.get("/diagnoses/{item_id}", response_model=Diagnoses, tags=["Diagnoses"])
def read_diagnosis(item_id: int, session: Session = Depends(get_session)):
    item = session.get(Diagnoses, item_id)
    if not item: raise HTTPException(status_code=404, detail="Not found")
    return item

@app.patch("/diagnoses/{item_id}", response_model=Diagnoses, tags=["Diagnoses"])
def update_diagnosis(item_id: int, update_data: DiagnosesUpdate, session: Session = Depends(get_session)):
    item = session.get(Diagnoses, item_id)
    if not item: raise HTTPException(status_code=404, detail="Not found")
    data = update_data.model_dump(exclude_unset=True)
    for key, value in data.items(): setattr(item, key, value)
    session.add(item); session.commit(); session.refresh(item)
    return item

@app.delete("/diagnoses/{item_id}", tags=["Diagnoses"])
def delete_diagnosis(item_id: int, session: Session = Depends(get_session)):
    item = session.get(Diagnoses, item_id)
    if not item: raise HTTPException(status_code=404, detail="Not found")
    session.delete(item); session.commit()
    return {"ok": True}


# 6. Appointment_Statuses
@app.post("/statuses/", response_model=Appointment_Statuses, tags=["Appointment Statuses"])
def create_status(item: Appointment_Statuses, session: Session = Depends(get_session)):
    session.add(item); session.commit(); session.refresh(item)
    return item

@app.get("/statuses/", response_model=List[Appointment_Statuses], tags=["Appointment Statuses"])
def read_statuses(session: Session = Depends(get_session)):
    return session.exec(select(Appointment_Statuses)).all()

@app.get("/statuses/{item_id}", response_model=Appointment_Statuses, tags=["Appointment Statuses"])
def read_status(item_id: int, session: Session = Depends(get_session)):
    item = session.get(Appointment_Statuses, item_id)
    if not item: raise HTTPException(status_code=404, detail="Not found")
    return item

@app.patch("/statuses/{item_id}", response_model=Appointment_Statuses, tags=["Appointment Statuses"])
def update_status(item_id: int, update_data: Appointment_StatusesUpdate, session: Session = Depends(get_session)):
    item = session.get(Appointment_Statuses, item_id)
    if not item: raise HTTPException(status_code=404, detail="Not found")
    data = update_data.model_dump(exclude_unset=True)
    for key, value in data.items(): setattr(item, key, value)
    session.add(item); session.commit(); session.refresh(item)
    return item

@app.delete("/statuses/{item_id}", tags=["Appointment Statuses"])
def delete_status(item_id: int, session: Session = Depends(get_session)):
    item = session.get(Appointment_Statuses, item_id)
    if not item: raise HTTPException(status_code=404, detail="Not found")
    session.delete(item); session.commit()
    return {"ok": True}


# 7. Doctors
@app.post("/doctors/", response_model=Doctors, tags=["Doctors"])
def create_doctor(item: Doctors, session: Session = Depends(get_session)):
    session.add(item); session.commit(); session.refresh(item)
    return item

@app.get("/doctors/", response_model=List[Doctors], tags=["Doctors"])
def read_doctors(session: Session = Depends(get_session)):
    return session.exec(select(Doctors)).all()

@app.get("/doctors/{item_id}", response_model=Doctors, tags=["Doctors"])
def read_doctor(item_id: int, session: Session = Depends(get_session)):
    item = session.get(Doctors, item_id)
    if not item: raise HTTPException(status_code=404, detail="Not found")
    return item

@app.patch("/doctors/{item_id}", response_model=Doctors, tags=["Doctors"])
def update_doctor(item_id: int, update_data: DoctorsUpdate, session: Session = Depends(get_session)):
    item = session.get(Doctors, item_id)
    if not item: raise HTTPException(status_code=404, detail="Not found")
    data = update_data.model_dump(exclude_unset=True)
    for key, value in data.items(): setattr(item, key, value)
    session.add(item); session.commit(); session.refresh(item)
    return item

@app.delete("/doctors/{item_id}", tags=["Doctors"])
def delete_doctor(item_id: int, session: Session = Depends(get_session)):
    item = session.get(Doctors, item_id)
    if not item: raise HTTPException(status_code=404, detail="Not found")
    session.delete(item); session.commit()
    return {"ok": True}


# 8. Insurance_Policies
@app.post("/policies/", response_model=Insurance_Policies, tags=["Insurance Policies"])
def create_policy(item: Insurance_Policies, session: Session = Depends(get_session)):
    session.add(item); session.commit(); session.refresh(item)
    return item

@app.get("/policies/", response_model=List[Insurance_Policies], tags=["Insurance Policies"])
def read_policies(session: Session = Depends(get_session)):
    return session.exec(select(Insurance_Policies)).all()

@app.get("/policies/{item_id}", response_model=Insurance_Policies, tags=["Insurance Policies"])
def read_policy(item_id: int, session: Session = Depends(get_session)):
    item = session.get(Insurance_Policies, item_id)
    if not item: raise HTTPException(status_code=404, detail="Not found")
    return item

@app.patch("/policies/{item_id}", response_model=Insurance_Policies, tags=["Insurance Policies"])
def update_policy(item_id: int, update_data: Insurance_PoliciesUpdate, session: Session = Depends(get_session)):
    item = session.get(Insurance_Policies, item_id)
    if not item: raise HTTPException(status_code=404, detail="Not found")
    data = update_data.model_dump(exclude_unset=True)
    for key, value in data.items(): setattr(item, key, value)
    session.add(item); session.commit(); session.refresh(item)
    return item

@app.delete("/policies/{item_id}", tags=["Insurance Policies"])
def delete_policy(item_id: int, session: Session = Depends(get_session)):
    item = session.get(Insurance_Policies, item_id)
    if not item: raise HTTPException(status_code=404, detail="Not found")
    session.delete(item); session.commit()
    return {"ok": True}


# 9. Patients
@app.post("/patients/", response_model=Patients, tags=["Patients"])
def create_patient(item: Patients, session: Session = Depends(get_session)):
    session.add(item); session.commit(); session.refresh(item)
    return item

@app.get("/patients/", response_model=List[Patients], tags=["Patients"])
def read_patients(session: Session = Depends(get_session)):
    return session.exec(select(Patients)).all()

@app.get("/patients/{item_id}", response_model=Patients, tags=["Patients"])
def read_patient(item_id: int, session: Session = Depends(get_session)):
    item = session.get(Patients, item_id)
    if not item: raise HTTPException(status_code=404, detail="Not found")
    return item

@app.patch("/patients/{item_id}", response_model=Patients, tags=["Patients"])
def update_patient(item_id: int, update_data: PatientsUpdate, session: Session = Depends(get_session)):
    item = session.get(Patients, item_id)
    if not item: raise HTTPException(status_code=404, detail="Not found")
    data = update_data.model_dump(exclude_unset=True)
    for key, value in data.items(): setattr(item, key, value)
    session.add(item); session.commit(); session.refresh(item)
    return item

@app.delete("/patients/{item_id}", tags=["Patients"])
def delete_patient(item_id: int, session: Session = Depends(get_session)):
    item = session.get(Patients, item_id)
    if not item: raise HTTPException(status_code=404, detail="Not found")
    session.delete(item); session.commit()
    return {"ok": True}


# 10. Schedule
@app.post("/schedules/", response_model=Schedule, tags=["Schedule"])
def create_schedule(item: Schedule, session: Session = Depends(get_session)):
    session.add(item); session.commit(); session.refresh(item)
    return item

@app.get("/schedules/", response_model=List[Schedule], tags=["Schedule"])
def read_schedules(session: Session = Depends(get_session)):
    return session.exec(select(Schedule)).all()

@app.get("/schedules/{item_id}", response_model=Schedule, tags=["Schedule"])
def read_schedule(item_id: int, session: Session = Depends(get_session)):
    item = session.get(Schedule, item_id)
    if not item: raise HTTPException(status_code=404, detail="Not found")
    return item

@app.patch("/schedules/{item_id}", response_model=Schedule, tags=["Schedule"])
def update_schedule(item_id: int, update_data: ScheduleUpdate, session: Session = Depends(get_session)):
    item = session.get(Schedule, item_id)
    if not item: raise HTTPException(status_code=404, detail="Not found")
    data = update_data.model_dump(exclude_unset=True)
    for key, value in data.items(): setattr(item, key, value)
    session.add(item); session.commit(); session.refresh(item)
    return item

@app.delete("/schedules/{item_id}", tags=["Schedule"])
def delete_schedule(item_id: int, session: Session = Depends(get_session)):
    item = session.get(Schedule, item_id)
    if not item: raise HTTPException(status_code=404, detail="Not found")
    session.delete(item); session.commit()
    return {"ok": True}


# 11. Appointments
@app.post("/appointments/", response_model=Appointments, tags=["Appointments"])
def create_appointment(item: Appointments, session: Session = Depends(get_session)):
    session.add(item); session.commit(); session.refresh(item)
    return item

@app.get("/appointments/", response_model=List[Appointments], tags=["Appointments"])
def read_appointments(session: Session = Depends(get_session)):
    return session.exec(select(Appointments)).all()

@app.get("/appointments/{item_id}", response_model=Appointments, tags=["Appointments"])
def read_appointment(item_id: int, session: Session = Depends(get_session)):
    item = session.get(Appointments, item_id)
    if not item: raise HTTPException(status_code=404, detail="Not found")
    return item

@app.patch("/appointments/{item_id}", response_model=Appointments, tags=["Appointments"])
def update_appointment(item_id: int, update_data: AppointmentsUpdate, session: Session = Depends(get_session)):
    item = session.get(Appointments, item_id)
    if not item: raise HTTPException(status_code=404, detail="Not found")
    data = update_data.model_dump(exclude_unset=True)
    for key, value in data.items(): setattr(item, key, value)
    session.add(item); session.commit(); session.refresh(item)
    return item

@app.delete("/appointments/{item_id}", tags=["Appointments"])
def delete_appointment(item_id: int, session: Session = Depends(get_session)):
    item = session.get(Appointments, item_id)
    if not item: raise HTTPException(status_code=404, detail="Not found")
    session.delete(item); session.commit()
    return {"ok": True}


# 12. Medical_Records
@app.post("/medical_records/", response_model=Medical_Records, tags=["Medical Records"])
def create_medical_record(item: Medical_Records, session: Session = Depends(get_session)):
    session.add(item); session.commit(); session.refresh(item)
    return item

@app.get("/medical_records/", response_model=List[Medical_Records], tags=["Medical Records"])
def read_medical_records(session: Session = Depends(get_session)):
    return session.exec(select(Medical_Records)).all()

@app.get("/medical_records/{item_id}", response_model=Medical_Records, tags=["Medical Records"])
def read_medical_record(item_id: int, session: Session = Depends(get_session)):
    item = session.get(Medical_Records, item_id)
    if not item: raise HTTPException(status_code=404, detail="Not found")
    return item

@app.patch("/medical_records/{item_id}", response_model=Medical_Records, tags=["Medical Records"])
def update_medical_record(item_id: int, update_data: Medical_RecordsUpdate, session: Session = Depends(get_session)):
    item = session.get(Medical_Records, item_id)
    if not item: raise HTTPException(status_code=404, detail="Not found")
    data = update_data.model_dump(exclude_unset=True)
    for key, value in data.items(): setattr(item, key, value)
    session.add(item); session.commit(); session.refresh(item)
    return item

@app.delete("/medical_records/{item_id}", tags=["Medical Records"])
def delete_medical_record(item_id: int, session: Session = Depends(get_session)):
    item = session.get(Medical_Records, item_id)
    if not item: raise HTTPException(status_code=404, detail="Not found")
    session.delete(item); session.commit()
    return {"ok": True}


# 13. Prescriptions
@app.post("/prescriptions/", response_model=Prescriptions, tags=["Prescriptions"])
def create_prescription(item: Prescriptions, session: Session = Depends(get_session)):
    session.add(item); session.commit(); session.refresh(item)
    return item

@app.get("/prescriptions/", response_model=List[Prescriptions], tags=["Prescriptions"])
def read_prescriptions(session: Session = Depends(get_session)):
    return session.exec(select(Prescriptions)).all()

@app.get("/prescriptions/{item_id}", response_model=Prescriptions, tags=["Prescriptions"])
def read_prescription(item_id: int, session: Session = Depends(get_session)):
    item = session.get(Prescriptions, item_id)
    if not item: raise HTTPException(status_code=404, detail="Not found")
    return item

@app.patch("/prescriptions/{item_id}", response_model=Prescriptions, tags=["Prescriptions"])
def update_prescription(item_id: int, update_data: PrescriptionsUpdate, session: Session = Depends(get_session)):
    item = session.get(Prescriptions, item_id)
    if not item: raise HTTPException(status_code=404, detail="Not found")
    data = update_data.model_dump(exclude_unset=True)
    for key, value in data.items(): setattr(item, key, value)
    session.add(item); session.commit(); session.refresh(item)
    return item

@app.delete("/prescriptions/{item_id}", tags=["Prescriptions"])
def delete_prescription(item_id: int, session: Session = Depends(get_session)):
    item = session.get(Prescriptions, item_id)
    if not item: raise HTTPException(status_code=404, detail="Not found")
    session.delete(item); session.commit()
    return {"ok": True}


# 14. Services_Rendered
@app.post("/services_rendered/", response_model=Services_Rendered, tags=["Services Rendered"])
def create_services_rendered(item: Services_Rendered, session: Session = Depends(get_session)):
    session.add(item); session.commit(); session.refresh(item)
    return item

@app.get("/services_rendered/", response_model=List[Services_Rendered], tags=["Services Rendered"])
def read_services_rendered(session: Session = Depends(get_session)):
    return session.exec(select(Services_Rendered)).all()

@app.get("/services_rendered/{item_id}", response_model=Services_Rendered, tags=["Services Rendered"])
def read_services_rendered_item(item_id: int, session: Session = Depends(get_session)):
    item = session.get(Services_Rendered, item_id)
    if not item: raise HTTPException(status_code=404, detail="Not found")
    return item

@app.patch("/services_rendered/{item_id}", response_model=Services_Rendered, tags=["Services Rendered"])
def update_services_rendered(item_id: int, update_data: Services_RenderedUpdate, session: Session = Depends(get_session)):
    item = session.get(Services_Rendered, item_id)
    if not item: raise HTTPException(status_code=404, detail="Not found")
    data = update_data.model_dump(exclude_unset=True)
    for key, value in data.items(): setattr(item, key, value)
    session.add(item); session.commit(); session.refresh(item)
    return item

@app.delete("/services_rendered/{item_id}", tags=["Services Rendered"])
def delete_services_rendered(item_id: int, session: Session = Depends(get_session)):
    item = session.get(Services_Rendered, item_id)
    if not item: raise HTTPException(status_code=404, detail="Not found")
    session.delete(item); session.commit()
    return {"ok": True}
