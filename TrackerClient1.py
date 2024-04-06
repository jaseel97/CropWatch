# client.py
import asyncio
import websockets
import random
import json

async def send_message():
    uri = "ws://localhost:8765"
    while True:
        try:
            async with websockets.connect(uri) as websocket:
                while True:
                    message = [random.randint(1,20), random.randint(0,100), random.randint(0,90)]
                    try:
                        await websocket.send(json.dumps(message))
                        print(f"Sent: {message}")
                    except:
                        print("Failed to send message. Retrying in 30 seconds...")
                        await asyncio.sleep(30)
                    await asyncio.sleep(5)
        except Exception as e:
            print(f"Failed to establish websocket connection: {e}")
            print("Retrying in 30 seconds...")
            await asyncio.sleep(30)

asyncio.run(send_message())