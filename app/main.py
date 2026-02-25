from fastapi import FastAPI,status,HTTPException
from pydantic import BaseModel

employees_db={}
employee_id_counter=1
app=FastAPI()

class Employee(BaseModel):
    full_name:str
    job_title:str
    country:str
    salary:float

class EmployeeResponse(Employee):
    employee_id:int











