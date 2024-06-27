# import pyfirmata
# from pyfirmata import Arduino, util
# import time
#
# port = 'COM3'
#
# board = Arduino(port)
#
# pin = board.get_pin('a:0:i')
#
# it = util.Iterator(board)
# it.start()
#
# while True:
#     heart_rate = pin.read()
#     print(heart_rate)
#     time.sleep(0.5)
#
#
# from pyfirmata import Arduino, util,INPUT
# import time

# port cinte command ls /dev/tty*
PORT = '/dev/ttyACM0'

# Initialize Arduino board
arduino_board = Arduino(PORT)
time.sleep(0.5)


pin = arduino_board.get_pin('a:0:i')

it = util.Iterator(arduino_board)
it.start()

while True:
    heart_rate = pin.read()
    print(heart_rate)
    time.sleep(0.5)

