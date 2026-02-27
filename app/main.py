from fastapi import FastAPI,status,HTTPException
from pydantic import BaseModel
from app.database import init_db,get_connection
from contextlib import asynccontextmanager

# employees_db={}
# employee_id_counter=1


@asynccontextmanager
async def lifespan(app:FastAPI):
    init_db()
    yield
app=FastAPI(lifespan=lifespan)
class Employee(BaseModel):
    full_name:str
    job_title:str
    country:str
    salary:float

class EmployeeResponse(Employee):
    employee_id:int

# def get_employee_or_404(employee_id:int):
#     employee=employees_db.get(employee_id)
#     if not employee:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Employee not found")
#     return employee

# @app.post("/employees",response_model=EmployeeResponse,status_code=status.HTTP_201_CREATED)
# def create_employee(employee:Employee):
#     global employee_id_counter
#     emp_id=employee_id_counter
#     employee_id_counter+=1
#     # employees_db[emp_id]=employee
#     conn = init_db()
#     cursor = conn.cursor()
#     cursor.execute(
#         "INSERT INTO employees (full_name, job_title, country, salary) VALUES (?, ?, ?, ?)",
#         (employee.full_name, employee.job_title, employee.country, employee.salary)
#     )
#     conn.commit()
#     emp_id = cursor.lastrowid
#     conn.close()
#
#     return EmployeeResponse(employee_id=emp_id,**employee.model_dump())

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

@app.put("/employees/{employee_id}",response_model=EmployeeResponse,status_code=status.HTTP_200_OK)
def update_employee(employee_id:int,employee:Employee):
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("""update employees set full_name=?,job_title=?,country=?,salary=? where employee_id=?""",
                   (employee.full_name,employee.job_title,employee.country,employee.salary,employee_id))
    conn.commit()
    cursor.execute("select * from employees where employee_id=?",(employee_id,))
    updated=cursor.fetchone()
    conn.close()
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Employee not found")
    return {"employee_id":updated[0],
            "full_name":updated[1],
            "job_title":updated[2],
            "country":updated[3],
            "salary":updated[4]}

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


# @app.get("/employees/{employee_id}",response_model=EmployeeResponse,status_code=status.HTTP_200_OK)
# def get_employee(employee_id:int):
#     employee=get_employee_or_404(employee_id)
#
#     return EmployeeResponse(employee_id=employee_id,**employee.model_dump())
#
# @app.put("/employees/{employee_id}",response_model=EmployeeResponse,status_code=status.HTTP_200_OK)
# def update_employee(employee_id:int,updated_employee:Employee):
#     get_employee_or_404(employee_id)
#     employees_db[employee_id]=updated_employee
#     return EmployeeResponse(employee_id=employee_id,**updated_employee.model_dump())


# @app.delete("/employees/{employee_id}",status_code=status.HTTP_204_NO_CONTENT)
# def delete_employee(employee_id:int):
#     if employee_id not in employees_db:
#         get_employee_or_404(employee_id)
#     employees_db.pop(employee_id)




