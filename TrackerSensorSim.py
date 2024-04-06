import serial
import time
import random

# COM port settings
COM_PORT = 'COM1'  # Change this to your COM port
BAUD_RATE = 9600

def generate_coordinates():
    # Generate random X and Y coordinates
    x = random.uniform(0, 100)
    y = random.uniform(0, 90)
    return x, y

def send_data(ser, data):
    ser.write(data.encode('utf-8'))

def main():
    try:
        ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=1)
        print(f"Connected to {COM_PORT}")
    except serial.SerialException:
        print(f"Failed to open {COM_PORT}. Make sure the port is available.")
        return

    try:
        while True:
            x, y = generate_coordinates()
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

            # Construct message
            message = f"$GPGGA,X,{x},Y,{y},{timestamp}\n"
            send_data(ser, message)
            print("Sent:", message.strip())

            time.sleep(10)

    except KeyboardInterrupt:
        print("Exiting...")
        ser.close()

if __name__ == "__main__":
    main()
