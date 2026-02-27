from fastapi import FastAPI,status,HTTPException
from pydantic import BaseModel,Field
from app.database import init_db,get_connection
from contextlib import asynccontextmanager
from app.database import init_db,get_connection
from app.repository import get_employee_by_id,update_employee_in_db
from app.services import validate_salary_update
from app.salary_service import calculate_deduction,calculate_salary_details
from typing import Optional
from app.salary_metrics import (get_salary_metrics_by_country,get_salary_metrics_by_job_title)
@asynccontextmanager
async def lifespan(app:FastAPI):
    init_db()
    yield
app=FastAPI(lifespan=lifespan)

class Employee(BaseModel):
    full_name:str
    job_title:str
    country:str
    salary:float=Field(gt=0)

class EmployeeResponse(Employee):
    employee_id:int


@app.post("/employees",response_model=EmployeeResponse,status_code=status.HTTP_201_CREATED)
def create_employee(employee:Employee):
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("insert into employees(full_name,job_title,country,salary) values (?,?,?,?)",
                   (employee.full_name,employee.job_title,employee.country,employee.salary))
    conn.commit()
    emp_id=cursor.lastrowid

    conn.close()
    return EmployeeResponse(employee_id=emp_id,**employee.model_dump())

@app.get("/employees/{employee_id}",response_model=EmployeeResponse,status_code=status.HTTP_200_OK)
def get_employee(employee_id:int):
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("""select * from employees where employee_id=?""",(employee_id,))
    row=cursor.fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Employee not found")
    conn.close()
    return EmployeeResponse(employee_id=row[0],
                            full_name=row[1],
                            job_title=row[2],
                            country=row[3],
                            salary=row[4])

@app.put("/employees/{employee_id}",response_model=EmployeeResponse)
def update_employee(employee_id:int,employee:Employee):

    existing=get_employee_by_id(employee_id)
    if not existing:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Employee not found")
    validate_salary_update(existing["salary"],employee.salary)
    updated=update_employee_in_db(employee_id=employee_id,employee=employee)

    return EmployeeResponse(employee_id=updated["employee_id"],
                            full_name=updated["full_name"],
                            job_title=updated["job_title"],
                            country=updated["country"],
                            salary=updated["salary"])


@app.delete("/employees/{employee_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(employee_id:int):
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("""select * from employees where employee_id=?""",(employee_id,))
    employee=cursor.fetchone()
    if not employee:
        conn.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Employee not found")
    cursor.execute("delete from employees where employee_id=?",(employee_id,))
    conn.commit()
    conn.close()




@app.get("/employees/{employee_id}/salary")
def calculate_salary(employee_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT country, salary FROM employees WHERE employee_id=?", (employee_id,))
    employee = cursor.fetchone()
    conn.close()

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    country, gross_salary = employee

    return calculate_salary_details(country,gross_salary)


@app.get("/metrics/salary")
def salary_metrics(country:Optional[str]=None,job_title:Optional[str]=None):
    if country:
        result=get_salary_metrics_by_country(country)
        if not result or result[0] is None:
            raise HTTPException(status_code=404,detail="Employee not found")
        return {"min_salary":result[0],
                "max_salary":result[1],
                "average_salary":result[2],}

    if job_title:
        result=get_salary_metrics_by_job_title(job_title)
        if not result or result[0] is None:
            raise HTTPException(status_code=404,detail="Employee not found")
        return {"average_salary":result[0],}

    raise HTTPException(status_code=400,detail="Must provide country or job title")

