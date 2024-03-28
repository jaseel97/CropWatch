import asyncio
import websockets
import json

from repo import create_connection

db_conn = create_connection()
cursor = db_conn.cursor()

async def echo(websocket, path):
    async for message in websocket:
        data = json.loads(message)
        print(data[0],data[1],data[2])
        query = "INSERT INTO location VALUES (%s,%s,%s);"
        cursor.execute(query,data)
        db_conn.commit()

start_server = websockets.serve(echo, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()