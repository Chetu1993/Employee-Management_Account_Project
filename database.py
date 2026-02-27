import sqlite3

dd_name="salary_management.db"
def get_connection():
    return sqlite3.connect(dd_name)

def create_table():
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("""create table if not exists employees(id integer primary key autoincrement,
    name text not null,salary real not null)""")
    conn.commit()
    conn.close()
