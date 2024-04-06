import asyncio
import websockets
import random
import json
import os
from nanoid import generate
import serial

tracker_id = 2
COM_PORT = 'COM2' 
BAUD_RATE = 9600
global ser

try:
    ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=1)
    print(f"Connected to {COM_PORT}")
except serial.SerialException:
    print(f"Failed to open {COM_PORT}. Make sure the port is available.")

def get_gps_data(ser):
    # while True:
        line = ser.readline().decode("utf-8").strip()
        if line.startswith("$GPGGA"):
            data_parts = line.split(",")
            latitude = float(data_parts[2]) if data_parts[2] else None
            longitude = float(data_parts[4]) if data_parts[4] else None
            timestamp = data_parts[5]
            return {
                "latitude": latitude,
                "longitude": longitude,
                "timestamp": timestamp
            }

async def send_message():
    uri = "ws://localhost:8765"
    while True:
        try:
            async with websockets.connect(uri) as websocket:
                while True:
                    try:
                        coordinates = get_gps_data(ser)
                        if coordinates is not None:
                            message = [tracker_id, coordinates['latitude'], coordinates['longitude']]
                            await websocket.send(json.dumps(message))
                            print(f"Sent: {message}")
                    except Exception as e:
                        print(f"Error: {e}")
                    finally:
                        await asyncio.sleep(10)
        except Exception as e:
            print(f"Failed to establish websocket connection: {e}")
            print("Retrying in 30 seconds...")
            await asyncio.sleep(30)

asyncio.run(send_message())
