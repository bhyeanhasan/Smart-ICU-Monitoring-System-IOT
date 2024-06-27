import json

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from .models import Sensors
from channels.db import database_sync_to_async
import asyncio


class TemperatureConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        print("Connected .... ")
        await self.accept()
        await self.send_json({'message': 'Connected'})

    async def receive_json(self, content, **kwargs):
        patient_temperature = content['temperature']
        ecg = content['ecg']
        time = content['time']

        print("TEMPERATURE: \t", patient_temperature)
        print("ECG: \t\t", ecg)
        print()

        # await self.send_json({'temperature': patient_temperature})
        sensors = Sensors()
        sensors.patient_temp = patient_temperature
        sensors.ecg = ecg
        sensors.time = time

        await database_sync_to_async(sensors.save)()

    async def close(self, code=None):
        print("Connection Closed ", code)


class DashboardConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        print("Connected .... ")
        await self.accept()
        await self.send_json({'message': 'Connected'})

    async def receive_json(self, content, **kwargs):
        async def get_objects():
            data = Sensors.objects.all()
            return data

        objects = await asyncio.to_thread(get_objects)
        cnt = 0
        print(objects)
        y = []
        x = []
        for object in objects:
            cnt += 1
            y.append(int(object.patient_temp))
            x.append(cnt)
        print(x)
        await self.send_json({'message': x})

    async def close(self, code=None):
        print("Connection Closed ", code)
        await self.send_json({'message': 'Connection Closed'})
