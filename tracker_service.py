import sqlite3
from config import get_config


config = get_config()

# def get_trackers(conn):
#     cursor = conn.cursor()
#     cursor.execute('''
#     SELECT * FROM trackers
#     ''')
#     trackers = []
#     for row in cursor:
#         trackers.append([row[0],row[1]])

#     return trackers

# def create_tracker(conn,tracker_id,assigned_to):
#     print(tracker_id,assigned_to)
#     query = '''
#         INSERT INTO trackers (id, assigned_to)
#         VALUES (%d, '%s')
#         ON CONFLICT (id)
#         DO UPDATE SET assigned_to = EXCLUDED.assigned_to'''%(tracker_id,assigned_to)
#     try:
#         cursor = conn.cursor()
#         cursor.execute(query)
#         conn.commit()
#         print("Updated tracker")
#     except:
#         print("Error upserting tracker")
#         return False
#     return True

# def delete_tracker(conn,tracker_id):
#     query = '''
#         DELETE FROM trackers WHERE id=%d
#     '''%(tracker_id)
#     try:
#         cursor = conn.cursor()
#         cursor.execute(query)
#         conn.commit()
#     except:
#         print("Error deleting tracker")
#         return False
#     return True

def lat_lon_to_pixel(latitude, longitude):
    map_width = config["map_width"]
    map_height = config["map_height"]
    min_lat = config["min_lat"]
    max_lat = config["max_lat"]
    min_lon = config["min_lon"]
    max_lon = config["max_lon"]

    lat_scale = (max_lat - min_lat) / map_height
    lon_scale = (max_lon - min_lon) / map_width

    lat_diff = latitude - min_lat
    lon_diff = longitude - min_lon

    y_pixel = lat_diff / lat_scale
    x_pixel = lon_diff / lon_scale

    return int(x_pixel), int(y_pixel)

# def get_coordinates(conn):
#     coordinates = {}
#     cursor = conn.cursor()
#     cursor.execute('''
#     WITH RecentLocations AS (
#     SELECT
#         tracker_id,
#         latitude,
#         longitude,
#         created_at,
#         ROW_NUMBER() OVER (PARTITION BY tracker_id ORDER BY created_at DESC) AS rn
#     FROM location
#     WHERE EXTRACT(EPOCH FROM (now() - created_at)) < 1800
#     )
#     SELECT t.assigned_to, rl.latitude, rl.longitude
#     FROM RecentLocations as rl
#     JOIN trackers as t ON t.id = rl.tracker_id
#     WHERE rn = 1;
#     ''')

#     for row in cursor:
#         x,y = lat_lon_to_pixel(row[1],row[2])
#         coordinates[row[0]] = {"x":x,"y":y}

#     return coordinates


# ##############################################################
def get_trackers(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM trackers')
        trackers = cursor.fetchall()  # Fetch all rows
        return trackers
    except sqlite3.Error as e:
        print("Error fetching trackers:", e)
        return []

def create_tracker(conn, tracker_id, assigned_to):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO trackers (id, assigned_to)
            VALUES (?, ?)
            ON CONFLICT (id) DO UPDATE SET assigned_to = excluded.assigned_to
        ''', (tracker_id, assigned_to))
        conn.commit()
        # print("Updated tracker")
        return True
    except sqlite3.Error as e:
        print("Error upserting tracker:", e)
        return False

def delete_tracker(conn, tracker_id):
    try:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM trackers WHERE id = ?', (tracker_id,))
        conn.commit()
        print("Deleted tracker")
        return True
    except sqlite3.Error as e:
        print("Error deleting tracker:", e)
        return False

def get_coordinates(conn):
    coordinates = {}
    try:
        cursor = conn.cursor()
        cursor.execute('''
        WITH RecentLocations AS (
            SELECT
                tracker_id,
                latitude,
                longitude,
                created_at,
                ROW_NUMBER() OVER (PARTITION BY tracker_id ORDER BY created_at DESC) AS rn
            FROM location
            WHERE STRFTIME('%s',datetime('now', 'localtime')) - STRFTIME('%s',datetime(created_at, 'localtime')) < 1800
        )
        SELECT t.assigned_to, rl.latitude, rl.longitude
        FROM RecentLocations AS rl
        JOIN trackers AS t ON t.id = rl.tracker_id
        WHERE rn = 1
        ''')

        for row in cursor:
            # Assuming `lat_lon_to_pixel` is a function defined elsewhere
            x, y = lat_lon_to_pixel(row[1], row[2])
            coordinates[row[0]] = {"x": x, "y": y}

        return coordinates
    except sqlite3.Error as e:
        print("Error fetching coordinates:", e)
        return {}