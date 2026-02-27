import sqlite3
db_name="employees.db"
def get_connection():
    return sqlite3.connect(db_name)

def init_db():
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("drop table if exists employees")
    cursor.execute("""create table employees (
                   employee_id integer primary key autoincrement,
                   full_name text not null,
                   job_title text not null,
                   country text not null,
                   salary real not null)""")

    conn.commit()

    conn.close()