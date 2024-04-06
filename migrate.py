from repo import create_connection

db_conn = create_connection()
cursor = db_conn.cursor()

# cursor.execute('''
#     DROP TABLE trackers
# ''')
# Create table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS trackers (
    id INTEGER PRIMARY KEY,
    assigned_to VARCHAR
)''')

# cursor.execute('''
#     DROP TABLE location
# ''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS location (
    tracker_id INTEGER,
    latitude NUMERIC,
    longitude NUMERIC,
    created_at timestamp DEFAULT now()
)''')

# cursor.execute('''
#     DROP TABLE zone_metrics
# ''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS zone_metrics (
    zone_id varchar,
    metric_name varchar,
    metric_value numeric,
    created_at timestamp default now()
)''')

db_conn.commit()
db_conn.close()