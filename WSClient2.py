# client.py
import asyncio
import websockets
import random
import json
import time


async def send_message():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        while True:
            message = ["emp2", random.randint(0,100), random.randint(0,100)]
            await websocket.send(json.dumps(message))
            print(f"Sent: {message}")
            await asyncio.sleep(5)

asyncio.run(send_message())