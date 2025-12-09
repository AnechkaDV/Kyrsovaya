from sqlmodel import SQLModel, create_engine, Session, select
from models import *  # Импортируем все модели
from datetime import date, time, datetime, timedelta
from decimal import Decimal

DATABASE_URL = "postgresql://postgres:b8TCN7-4WJ@localhost/polyclinic_db"

engine = create_engine(DATABASE_URL)

def create_db_and_tables():
    """Создает таблицы в БД на основе моделей"""
    SQLModel.metadata.create_all(engine)

def populate_data():
    """Наполняет БД тестовыми данными"""
    with Session(engine) as session:
        # 1. Справочники
        spec_ter = Specializations(name="Терапевт")
        spec_hir = Specializations(name="Хирург")
        dept_main = Departments(name="Общее отделение")
        
        status_planned = Appointment_Statuses(name="Запланирован")
        status_completed = Appointment_Statuses(name="Завершен")
        
        diag_flu = Diagnoses(mkb_code="J10", description="Грипп")
        
        session.add_all([spec_ter, spec_hir, dept_main, status_planned, status_completed, diag_flu])
        session.commit() # Чтобы получить ID

        # 2. Врачи и Кабинеты
        cab_101 = Cabinets(number="101", floor=1, department_id=dept_main.id)
        session.add(cab_101)
        session.commit()

        doc_ivanov = Doctors(
            last_name="Иванов", first_name="Иван", middle_name="Иванович",
            specialization_id=spec_ter.id, department_id=dept_main.id, category="Высшая"
        )
        session.add(doc_ivanov)
        session.commit()

        # 3. Пациенты
        policy_1 = Insurance_Policies(policy_number="1234567890", company_name="РОСНО", expiration_date=date(2030, 1, 1))
        session.add(policy_1)
        session.commit()

        pat_petrov = Patients(
            last_name="Петров", first_name="Петр", birth_date=date(1990, 5, 15),
            phone="+79001234567", policy_id=policy_1.id
        )
        session.add(pat_petrov)
        session.commit()

        appt_time = datetime.now().replace(hour=10, minute=0, second=0, microsecond=0) + timedelta(days=1)
        appt = Appointments(
            patient_id=pat_petrov.id, doctor_id=doc_ivanov.id,
            datetime=appt_time, status_id=status_planned.id
        )
        session.add(appt)
        session.commit()
        
        print("База данных успешно наполнена тестовыми данными!")

def run_queries():
    """Примеры выборок данных"""
    with Session(engine) as session:
        print("\n--- 1. Список всех врачей со специальностями ---")
        statement = select(Doctors, Specializations).join(Specializations)
        results = session.exec(statement).all()
        for doctor, spec in results:
            print(f"Врач: {doctor.last_name} {doctor.first_name}, Специальность: {spec.name}")

        print("\n--- 2. Найти всех пациентов, записанных к Иванову ---")
        # Ищем врача по фамилии
        doc_id = session.exec(select(Doctors.id).where(Doctors.last_name == "Иванов")).first()
        
        if doc_id:
            statement = select(Appointments, Patients).where(Appointments.doctor_id == doc_id).join(Patients)
            results = session.exec(statement).all()
            for appt, patient in results:
                print(f"Пациент: {patient.last_name}, Время приема: {appt.datetime}")
        
        print("\n--- 3. Детали медицинской карты (если есть) ---")
        pass

if __name__ == "__main__":
    # 1. Создание таблиц
    create_db_and_tables()
    
    # 2. Наполнение данными (раскомментировать при первом запуске)
    populate_data()
    
    # 3. Выполнение запросов
    run_queries()
