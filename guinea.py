import sqlite3
from datetime import datetime, timedelta

# Function to group datetime by cadence
def group_by_cadence(dt, cadence):
    if cadence == 'hour':
        return dt.replace(minute=0, second=0, microsecond=0)
    elif cadence == 'day':
        return dt.replace(hour=0, minute=0, second=0, microsecond=0)
    elif cadence == 'week':
        return dt - timedelta(days=dt.weekday())
    elif cadence == 'month':
        return dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

# Function to query database and group data by cadence
def query_database(start_date, end_date, cadence):
    conn = sqlite3.connect('TestDB.db')  # Replace 'your_database.db' with your database file
    c = conn.cursor()

    # Prepare SQL query
    query = f"""
            SELECT zone_id, metric_name, metric_value, created_at
            FROM zone_metrics
            WHERE created_at BETWEEN ? AND ?
            """

    # Execute SQL query
    c.execute(query, (start_date, end_date))

    # Group data by cadence
    grouped_data = {}
    for row in c.fetchall():
        zone_id, metric_name, metric_value, start_date = row
        cadence_group = group_by_cadence(start_date, cadence)
        if cadence_group not in grouped_data:
            grouped_data[cadence_group] = []
        grouped_data[cadence_group].append((zone_id, metric_name, metric_value, start_date))

    conn.close()
    return grouped_data

# Example usage
start_date = datetime(2024, 4, 1)
end_date = datetime(2024, 4, 30)
cadence = 'day'

result = query_database(start_date, end_date, cadence)
for cadence_group, data in result.items():
    print(f"Cadence: {cadence_group}, Data: {data}")