import sqlite3
db_name="employees.db"
def get_connection():
    conn=sqlite3.connect(db_name)
    conn.row_factory=sqlite3.Row
    return conn

def init_db():
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("""create table if not exists employees (
                   employee_id integer primary key autoincrement,
                   full_name text not null,
                   job_title text not null,
                   country text not null,
                   salary real not null)""")

    conn.commit()

    conn.close()