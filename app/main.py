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

def get_employee_or_404(employee_id:int):
    employee=employees_db.get(employee_id)
    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Employee not found")
    return employee

@app.post("/employees",response_model=EmployeeResponse,status_code=status.HTTP_201_CREATED)
def create_employee(employee:Employee):
    global employee_id_counter
    emp_id=employee_id_counter
    employee_id_counter+=1
    employees_db[emp_id]=employee
    return EmployeeResponse(employee_id=emp_id,**employee.model_dump())

@app.get("/employees/{employee_id}",response_model=EmployeeResponse,status_code=status.HTTP_200_OK)
def get_employee(employee_id:int):
    employee=get_employee_or_404(employee_id)

    return EmployeeResponse(employee_id=employee_id,**employee.model_dump())

@app.put("/employees/{employee_id}",response_model=EmployeeResponse,status_code=status.HTTP_200_OK)
def update_employee(employee_id:int,updated_employee:Employee):
    get_employee_or_404(employee_id)
    employees_db[employee_id]=updated_employee
    return EmployeeResponse(employee_id=employee_id,**updated_employee.model_dump())


@app.delete("/employees/{employee_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(employee_id:int):
    if employee_id not in employees_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Employee not found")
    del employees_db[employee_id]




