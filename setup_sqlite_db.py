import sqlite3

#'FarmMonitor.db'
def create_sqlite_connection(db):
    conn = None
    try:
        conn = sqlite3.connect(db,check_same_thread=False)
        print(sqlite3.version)
    except sqlite3.Error as e:
        print(e)
        return

    return conn

create_trackers = '''CREATE TABLE IF NOT EXISTS trackers (
    id INTEGER PRIMARY KEY,
    assigned_to TEXT
);'''

create_location = '''CREATE TABLE IF NOT EXISTS location (
    tracker_id INTEGER,
    latitude NUMERIC,
    longitude NUMERIC,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);'''

create_zone_metrics = '''CREATE TABLE IF NOT EXISTS zone_metrics (
    zone_id TEXT,
    metric_name TEXT,
    metric_value NUMERIC,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)'''


dummy_trackers = ''' INSERT INTO trackers(id,assigned_to) VALUES(?,?) '''
dummy_location = ''' INSERT INTO location(tracker_id,latitude,longitude) VALUES(?,?,?) '''
dummy_metrics = ''' INSERT INTO zone_metrics(zone_id,metric_name,metric_value) VALUES(?,?,?) '''


conn = create_sqlite_connection('TestDB.db')
cur = conn.cursor()

cur.execute(create_trackers)
cur.execute(create_location)
cur.execute(create_zone_metrics)

# cur.execute(dummy_trackers,(1,"EmployeeA"))
# cur.execute(dummy_trackers,(2,"EmployeeB"))
# cur.execute(dummy_trackers,(3,"EmployeeC"))

# cur.execute(dummy_location,(1,55,55))
# cur.execute(dummy_location,(2,35,50))
# cur.execute(dummy_location,(3,60,60))

# cur.execute(dummy_location,(1,"temperature",25))
# cur.execute(dummy_location,(1,"temperature",27))
# cur.execute(dummy_location,(2,"moisture",0.5))
# cur.execute(dummy_location,(2,"moisture",0.6))

conn.commit()

conn.close()
