import serial
import time

PORT = 'COM11'  # Change this to your Arduino port
BAUD_RATE = 9600
TIMEOUT = 2  # Set a timeout for the serial connection


ir_lst = []
red_lst = []
def read_from_arduino(port, baud_rate, timeout):
    try:
        ser = serial.Serial(port, baud_rate, timeout=timeout)
        time.sleep(2)  # Wait for Arduino to initialize
        print("Serial connection established")

        while True:
            if ser.in_waiting > 0:
                try:
                    line = ser.readline().decode('utf-8').strip()

                    if line:
                        if line.startswith("IR:"):
                            data = line.split(",")
                            ir = data[0].split(":")[1].strip()
                            red = data[1].split(":")[1].strip()

                            ir_lst.append(ir)
                            red_lst.append(red)

                            print(f"IR: {ir}, RED: {red}")
                    else:
                        print("Received empty line")
                except Exception as e:
                    print(f"Error reading line: {e}")
            else:
                print("Waiting for data...")
            time.sleep(1)
    except serial.SerialException as e:
        print(f"Serial error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        ser.close()
        print("Serial connection closed")

if __name__ == "__main__":
    read_from_arduino(PORT, BAUD_RATE, TIMEOUT)
