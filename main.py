import datetime
import sqlalchemy
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import IntegrityError

app = FastAPI()

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://isp_p_Sedunov:12345@77.91.86.135/isp_p_Sedunov"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Employee(Base):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True, index=True)
    department_code = Column(Integer)
    full_name = Column(String)
    position = Column(String)
    salary = Column(Float)
    bonus = Column(Float)
    month = Column(String)


class Contract(Base):
    __tablename__ = 'contracts'

    id = Column(Integer, primary_key=True, index=True)
    number = Column(String, unique=True)
    organization_name = Column(String)
    date_signed = Column(Date)
    employee_id = Column(Integer, ForeignKey('employees.id'))


class Organization(Base):
    __tablename__ = 'organizations'

    id = Column(Integer, primary_key=True, index=True)
    contract_id = Column(Integer, ForeignKey('contracts.id'))
    country_code = Column(String)
    city = Column(String)
    address = Column(String)
    phone = Column(String)
    email = Column(String)
    website = Column(String)

class Delivery(Base):
    __tablename__ = 'deliveries'

    id = Column(Integer, primary_key=True, index=True)
    contract_id = Column(Integer, ForeignKey('contracts.id'))
    equipment_type = Column(String)
    user_comment = Column(String)
    employee_id = Column(Integer, ForeignKey('employees.id'))

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_employee(db: Session, employee: EmployeeCreate):
    db_employee = Employee(**employee.dict())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee


def read_employee(db: Session, employee_id: int):
    return db.query(Employee).filter(Employee.id == employee_id).first()


def update_employee(db: Session, employee_id: int, employee_update: EmployeeUpdate):
    db_employee = db.query(Employee).filter(Employee.id == employee_id).first()
    for key, value in employee_update.dict().items():
        setattr(db_employee, key, value)
    db.commit()
    db.refresh(db_employee)
    return db_employee


def delete_employee(db: Session, employee_id: int):
    db_employee = db.query(Employee).filter(Employee.id == employee_id).first()
    db.delete(db_employee)
    db.commit()
    return {'detail': 'Employee deleted'}