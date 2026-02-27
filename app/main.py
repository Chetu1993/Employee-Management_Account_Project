from fastapi import FastAPI,status,HTTPException
from pydantic import BaseModel,Field
from app.database import init_db,get_connection
from contextlib import asynccontextmanager
from app.database import init_db,get_connection

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
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("select * from employees where employee_id=?",(employee_id,))
    conn.commit()
    cursor.execute("select * from employees where employee_id=?",(employee_id,))
    existing=cursor.fetchone()
    if not existing:
        conn.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Employee not found")
    if employee.salary<existing["salary"]:
        conn.close()
        raise HTTPException(status_code=400,detail="Salary cannout decrease")
    cursor.execute("""update employees set full_name=?,job_title=?,country=?,salary=? where employee_id=?""",
                   (employee.full_name,employee.job_title,employee.country,employee.salary,employee_id))
    conn.commit()
    cursor.execute("select * from employees where employee_id=?",(employee_id,))
    updated=cursor.fetchone()
    conn.close()
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






