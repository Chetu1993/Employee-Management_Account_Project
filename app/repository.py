from app.database import get_connection


def get_employee_by_id(employee_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees WHERE employee_id=?", (employee_id,))
    employee = cursor.fetchone()
    conn.close()
    return employee


def update_employee_in_db(employee_id: int, employee):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE employees
        SET full_name=?, job_title=?, country=?, salary=?
        WHERE employee_id=?
        """,
        (employee.full_name, employee.job_title, employee.country, employee.salary, employee_id)
    )
    conn.commit()

    cursor.execute("SELECT * FROM employees WHERE employee_id=?", (employee_id,))
    updated = cursor.fetchone()
    conn.close()
    return updated