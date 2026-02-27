from app.database import get_connection


def get_salary_metrics_by_country(country: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT MIN(salary), MAX(salary), AVG(salary) FROM employees WHERE country=?",
        (country,)
    )
    result = cursor.fetchone()
    conn.close()
    return result


def get_salary_metrics_by_job_title(job_title: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT AVG(salary) FROM employees WHERE job_title=?",
        (job_title,)
    )
    result = cursor.fetchone()
    conn.close()
    return result