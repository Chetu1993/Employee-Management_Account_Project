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


@app.post("/employees",response_model=EmployeeResponse,status_code=status.HTTP_201_CREATED)
def create_employee(employee:Employee):
    global employee_id_counter
    emp_id=employee_id_counter
    employee_id_counter+=1
    employees_db[emp_id]=employee
    return EmployeeResponse(employee_id=emp_id,**employee.model_dump())





