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
    temp_fahrenheit = (temp_celsius * 9/5) + 32
    return temp_fahrenheit


try:
	# Initialize the sensor
	max30102_setup()

	while True:
		# Read heart rate and SpO2 from MAX30102
		ir, red = read_max30102_data()
		temperature = read_temperature()

		print(ir,red)
		print(temperature)

		print("ok")



except KeyboardInterrupt:
	print("\nProgram stopped by user")
