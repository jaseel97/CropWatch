from repo import create_connection

db_conn = create_connection()
cursor = db_conn.cursor()

cursor.execute("DROP TABLE location")
db_conn.commit()
# Create table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS location (
    employee_id TEXT PRIMARY KEY,
    gps_x INTEGER NOT NULL,
    gps_y INTEGER NOT NULL
)''')

cursor.execute('''
    INSERT INTO location VALUES
    ('emp1',50,50),
    ('emp2',60,50),
    ('emp3',30,40);
''')
db_conn.commit()
db_conn.close()
