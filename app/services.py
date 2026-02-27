from fastapi import HTTPException


def validate_salary_update(old_salary: float, new_salary: float):
    if new_salary < old_salary:
        raise HTTPException(status_code=400, detail="Salary cannot decrease")