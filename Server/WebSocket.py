import json
import time
import board
import asyncio
import websockets
import busio as io
import adafruit_mlx90614
from datetime import datetime
from pyfirmata import Arduino, util

# **************************** please ensure IP is correct ***************************** #
link = 'ws://192.168.192.62:8000/ws/temperature/'
# ************************************************************************************** #

# ************************************ temperature ************************************* #
# i2c = io.I2C(board.SCL, board.SDA, frequency=100000)
# mlx = adafruit_mlx90614.MLX90614(i2c)
# ************************************************************************************** #

import smbus
import time
import numpy as np

# Define I2C bus (1 on Raspberry Pi 3/4, 0 on earlier versions)
bus = smbus.SMBus(1)

mlx90614_address = 0x5A
max30102_address = 0x57

# MAX30102 Registers
REG_INTR_STATUS_1 = 0x00
REG_INTR_STATUS_2 = 0x01
REG_INTR_ENABLE_1 = 0x02
REG_INTR_ENABLE_2 = 0x03
REG_FIFO_WR_PTR = 0x04
REG_OVF_COUNTER = 0x05
REG_FIFO_RD_PTR = 0x06
REG_FIFO_DATA = 0x07
REG_FIFO_CONFIG = 0x08
REG_MODE_CONFIG = 0x09
REG_SPO2_CONFIG = 0x0A
REG_LED1_PA = 0x0C
REG_LED2_PA = 0x0D
REG_PILOT_PA = 0x10


# Initialize MAX30102
def max30102_setup():
	# Reset the sensor
	bus.write_byte_data(max30102_address, REG_MODE_CONFIG, 0x40)
	time.sleep(0.1)

	# Clear the FIFO pointers
	bus.write_byte_data(max30102_address, REG_FIFO_WR_PTR, 0x00)
	bus.write_byte_data(max30102_address, REG_OVF_COUNTER, 0x00)
	bus.write_byte_data(max30102_address, REG_FIFO_RD_PTR, 0x00)

	# Configure the sensor
	bus.write_byte_data(max30102_address, REG_INTR_ENABLE_1, 0xc0)  # A_FULL_EN and PPG_RDY_EN
	bus.write_byte_data(max30102_address, REG_INTR_ENABLE_2, 0x00)
	bus.write_byte_data(max30102_address, REG_FIFO_CONFIG,
						0x4f)  # sample average = 4, FIFO rollover = enable, FIFO almost full = 17
	bus.write_byte_data(max30102_address, REG_MODE_CONFIG, 0x03)  # Heart rate and SpO2 mode
	bus.write_byte_data(max30102_address, REG_SPO2_CONFIG,
						0x27)  # SPO2 ADC range = 4096nA, SPO2 sample rate (100 Hz), LED pulseWidth (411uS)
	bus.write_byte_data(max30102_address, REG_LED1_PA, 0x24)  # LED1 = 7.6mA
	bus.write_byte_data(max30102_address, REG_LED2_PA, 0x24)  # LED2 = 7.6mA


# Function to read heart rate and SpO2 from MAX30102
def read_max30102_data():
	# Read FIFO data registers (6 bytes)
	data = bus.read_i2c_block_data(max30102_address, REG_FIFO_DATA, 6)

	# Combine the bytes to get IR and Red values
	ir = (data[0] << 16) | (data[1] << 8) | data[2]
	red = (data[3] << 16) | (data[4] << 8) | data[5]

	return ir, red


def read_temperature():
	# Read from MLX90614 (ambient temperature register)
	temp_data = bus.read_i2c_block_data(mlx90614_address, 0x07, 2)
	temp_raw = (temp_data[1] << 8) | temp_data[0]
	temp_celsius = (temp_raw * 0.02) - 273.15
	temp_fahrenheit = (temp_celsius * 9 / 5) + 32
	return temp_fahrenheit


# *************************************** ECG ****************************************** #
PORT = '/dev/ttyACM0'
arduino_board = Arduino(PORT)
time.sleep(0.5)
ecg_pin = arduino_board.get_pin('a:0:i')
gsr_pin = arduino_board.get_pin('a:2:i')
hr_pin = arduino_board.get_pin('a:4:i')
it = util.Iterator(arduino_board)
it.start()


# ************************************************************************************** #

async def main():
	try:
		while 1:
			async with websockets.connect(link) as websocket:
				print("Connected With Server ... ")
				while 1:
					try:
						# ambientTemp = "{:.2f}".format(mlx.ambient_temperature * (9.0 / 5.0) + 32)
						# targetTemp = "{:.2f}".format(mlx.object_temperature * (9.0 / 5.0) + 32)
						# print("TEMP \t: " + str(targetTemp))
						# time.sleep(0.5)

						ir, red = read_max30102_data()
						time.sleep(0.5)
						temperature = read_temperature()
						time.sleep(0.5)

						ecg = ecg_pin.read()
						print("ECG \t: " + str(ecg))
						time.sleep(0.5)

						gsr = gsr_pin.read()
						print("GSR \t: " + str(gsr))
						time.sleep(0.5)

						hr = hr_pin.read()
						print("HR \t: " + str(hr))
						time.sleep(0.5)

						# DATA PASSING
						data = json.dumps({
							'temperature': str(temperature),
							'ecg': str(ecg),
							'gsr': str(gsr),
							'hr': str(hr * 100),
							'ir': str(ir),
							'red': str(red),
							'time': str(datetime.now())
						})
						await websocket.send(data)
						print('Data Updated\n')
						time.sleep(1)
					except Exception as e:
						print(e)
						break
	except:
		print("Connection Error")


asyncio.get_event_loop().run_until_complete(main())
