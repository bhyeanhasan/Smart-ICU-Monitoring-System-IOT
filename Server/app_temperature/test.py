import asyncio
import json
import random
import time
import websockets
from datetime import datetime

link = 'ws://192.168.0.105:8000/ws/temperature/'


async def main():
    try:
        async with websockets.connect(link) as websocket:
            print("Connected ... ")
            while 1:
                try:
                    data = json.dumps({
                        'temperature': str(random.randint(100, 500)),
                        'time': str(datetime.now())
                    })
                    await websocket.send(data)
                    print('data updated')
                    time.sleep(5)  # wait and then do it again
                except Exception as e:
                    print(e)
    except:
        print("Connection Error")


asyncio.get_event_loop().run_until_complete(main())
