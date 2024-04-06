import asyncio
import websockets
import json

from repo import create_connection, create_sqlite_connection

# db_conn = create_connection()
db_conn = create_sqlite_connection()
cursor = db_conn.cursor()

async def echo(websocket, path):
    try:
        async for message in websocket:
            data = json.loads(message)
            print(data[0], data[1], data[2])
            # query = "INSERT INTO location(tracker_id, latitude, longitude) VALUES (%s, %s, %s);"
            query = "INSERT INTO location(tracker_id, latitude, longitude) VALUES (?, ?, ?);"
            cursor.execute(query, data)
            db_conn.commit()
    except KeyboardInterrupt:
        print("Shutting down gracefully...")
        await websocket.close()
        cursor.close()
        db_conn.close()

start_server = websockets.serve(echo, "localhost", 8765)

try:
    print("Employee Tracker Running...")
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
except KeyboardInterrupt:
    pass
finally:
    asyncio.get_event_loop().close()
