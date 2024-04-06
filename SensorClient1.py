# import time
# from w1thermsensor import W1ThermSensor
# import Adafruit_ADS1x15

# sensor = W1ThermSensor() #DS18B20

# while True:
#     temperature = sensor.get_temperature()
#     print("The temperature is %s celsius" % temperature)
#     time.sleep(1)

import asyncio
import websockets
import random
import json
import os
from nanoid import generate
import serial

zone_id = "1"
sensor_uri = "ws://localhost:8766"

def get_temperature_data():
    return random.uniform(-10, 35)

def get_moisture_data():
    return random.uniform(0,1)

async def send_message():
    async with websockets.connect(sensor_uri) as websocket:
        while True:
            try :
                temperature = get_temperature_data()
                moisture = get_moisture_data()
                # message = [zone_id, round(temperature,2), round(moisture,2)]
                message = [random.randint(1,4), round(temperature,2), round(moisture,2)]
                await websocket.send(json.dumps(message))
                print(f"Sent: {message}")
            except:
                print("error pinging coordinates")
            finally:
                await asyncio.sleep(30)

asyncio.run(send_message())



