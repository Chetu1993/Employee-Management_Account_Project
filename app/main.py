from fastapi import FastAPI,status,HTTPException
from pydantic import BaseModel,Field

from contextlib import asynccontextmanager



from app.database import init_db,get_connection
from app.repository import get_employee_by_id,update_employee_in_db
from app.services import validate_salary_update
from app.salary_service import calculate_salary_details
from typing import Optional,List
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
    with get_connection() as conn:
        cursor=conn.cursor()
        cursor.execute("insert into employees(full_name,job_title,country,salary) values (?,?,?,?)",
                   (employee.full_name,employee.job_title,employee.country,employee.salary))
        conn.commit()
        emp_id=cursor.lastrowid


        return EmployeeResponse(employee_id=emp_id,**employee.model_dump())

@app.get("/employees/{employee_id}",response_model=EmployeeResponse,status_code=status.HTTP_200_OK)
def get_employee(employee_id:int):
    with get_connection() as conn:
        cursor=conn.cursor()
        cursor.execute("""select * from employees where employee_id=?""",(employee_id,))
        row=cursor.fetchone()
        if not row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Employee not found")
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
    with get_connection() as conn:
        cursor=conn.cursor()
        cursor.execute("""select * from employees where employee_id=?""",(employee_id,))
        employee=cursor.fetchone()
        if not employee:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Employee not found")
        cursor.execute("delete from employees where employee_id=?",(employee_id,))
        conn.commit()





@app.get("/employees/{employee_id}/salary")
def calculate_salary(employee_id: int):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT country, salary FROM employees WHERE employee_id=?", (employee_id,))
        employee = cursor.fetchone()
        if not employee:
            raise HTTPException(status_code=404, detail="Employee not found")

        country, gross_salary = employee

    return calculate_salary_details(country,gross_salary)


@app.get("/metrics/salary")
def salary_metrics(country:Optional[str]=None,job_title:Optional[str]=None):
    if country and job_title:
        raise HTTPException(
            status_code=400,
            detail="Provide either country or job_title, not both"
        )

    if not country and not job_title:
        raise HTTPException(
            status_code=400,
            detail="Must provide country or job_title"
        )
    if country:
        result=get_salary_metrics_by_country(country)
        if not result or result[0] is None:
            raise HTTPException(status_code=404,detail="No salary found for a given data")
        return {"min_salary":result[0],
                "max_salary":result[1],
                "average_salary":result[2]}

    if job_title:
        result=get_salary_metrics_by_job_title(job_title)
        if not result or result[0] is None:
            raise HTTPException(status_code=404,detail="No salary found for a given data")
        return {"average_salary":result[0]}

@app.get("/employees",response_model=List[EmployeeResponse])
def get_all_employees():
    with get_connection() as conn:
        cursor=conn.cursor()
        cursor.execute("select * from employees")
        rows=cursor.fetchall()

    return [EmployeeResponse(
        employee_id=row["employee_id"],
        full_name=row["full_name"],
        job_title=row["job_title"],
        country=row["country"],
        salary=row["salary"]
    )for row in rows]

















