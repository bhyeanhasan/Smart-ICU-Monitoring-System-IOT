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
link = 'ws://192.168.35.62:8000/ws/temperature/'
# ************************************************************************************** #

# ************************************ temperature ************************************* #
i2c = io.I2C(board.SCL, board.SDA, frequency=100000)
mlx = adafruit_mlx90614.MLX90614(i2c)
# ************************************************************************************** #

# *************************************** Arduino ****************************************** #
PORT = '/dev/ttyACM0'
arduino_board = Arduino(PORT)
time.sleep(0.5)
ecg_pin = arduino_board.get_pin('a:0:i')
gsr_pin = arduino_board.get_pin('a:2:i')
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
                        targetTemp = "{:.2f}".format(mlx.object_temperature * (9.0 / 5.0) + 32)
                        print("TEMP : " + targetTemp)
                        time.sleep(0.5)

                        ecg = ecg_pin.read()
                        print("ECG : " + ecg)
                        time.sleep(0.5)

                        gsr = gsr_pin.read()
                        print("GSR : " + gsr)
                        time.sleep(0.5)

                        # DATA PASSING
                        data = json.dumps({
                            'temperature': str(targetTemp),
                            'ecg': str(ecg),
                            'gsr': str(gsr),
                            'time': str(datetime.now())
                        })
                        await websocket.send(data)
                        print('Data Updated')
                        time.sleep(1)
                    except Exception as e:
                        print(e)
                        break
    except:
        print("Connection Error")


asyncio.get_event_loop().run_until_complete(main())
