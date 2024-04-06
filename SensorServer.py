import asyncio
from datetime import datetime
import os
import pandas as pd
import websockets
import json

from repo import create_connection, create_sqlite_connection

# db_conn = create_connection()
db_conn = create_sqlite_connection()
cursor = db_conn.cursor()

def save_to_csv(dataframe, filename):
    file_exists = os.path.isfile(filename)
    dataframe.to_csv(filename, mode='a', header=not file_exists, index=False)

async def echo(websocket):
    try:
        async for message in websocket:
            timestamp = datetime.now()
            data = json.loads(message)
            print(data[0], data[1], data[2])
            # query = "INSERT INTO zone_metrics(zone_id, metric_name, metric_value) VALUES (%s, %s, %s);"
            query = "INSERT INTO zone_metrics(zone_id, metric_name, metric_value) VALUES (?, ?, ?)"
            cursor.execute(query, [data[0],"temperature",data[1]])
            cursor.execute(query, [data[0],"moisture",data[2]])
            db_conn.commit()
            data = {'ZoneId': [1, 1], 
            'MetricName': ['temperature', 'moisture'], 
            'MetricValue': [data[1], data[2]], 
            'Timestamp': [timestamp, timestamp]}
            df = pd.DataFrame(data)
            save_to_csv(df,"historic.csv")

    except KeyboardInterrupt:
        print("Shutting down gracefully...")
        await websocket.close()
        cursor.close()
        db_conn.close()

start_server = websockets.serve(echo, "localhost", 8766)

try:
    print("Sensor Data Tracker Running...")
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
except KeyboardInterrupt:
    pass
finally:
    asyncio.get_event_loop().close()
