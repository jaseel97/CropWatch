from repo import create_connection

db_conn = create_connection()
cursor = db_conn.cursor()

# Create table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS employee (
    id VARCHAR PRIMARY KEY,
    name VARCHAR,
    role VARCHAR
)''')

cursor.execute('''
    DROP TABLE location
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS location (
    employee_id TEXT,
    x INTEGER NOT NULL,
    y INTEGER NOT NULL,
    created_at timestamp default now()
)''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS zone_metrics (
    zone_id TEXT PRIMARY KEY,
    metric_name varchar,
    metric_value numeric,
    created_at timestamp default now()
)''')



db_conn.commit()
db_conn.close()