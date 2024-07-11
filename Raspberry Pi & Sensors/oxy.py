import serial
import time

port2 = '/dev/ttyACM1'  # Change this to your Arduino port
baud_rate = 9600

def read_from_arduino(port, baud_rate):
    ser = serial.Serial(port2, baud_rate)
    time.sleep(2)  # Wait for Arduino to initialize

    try:
        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').strip()
                if line.startswith("IR:"):
                    data = line.split(",")
                    ir = data[0].split(":")[1].strip()
                    red = data[1].split(":")[1].strip()
                    print(f"IR: {ir}, RED: {red}")
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Program interrupted")
    finally:
        ser.close()

if __name__ == "__main__":
    read_from_arduino(PORT, BAUD_RATE)
