import json

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from .models import Temperature
from channels.db import database_sync_to_async
import asyncio


class TemperatureConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        print("Connected .... ")
        await self.accept()
        await self.send_json({'message': 'Connected'})

    async def receive_json(self, content, **kwargs):
        patient_temperature = content['temperature']
        time = content['time']
        print(patient_temperature)
        await self.send_json({'temperature': patient_temperature})
        temperature = Temperature()
        temperature.patient_temp = patient_temperature
        temperature.time = time
        await database_sync_to_async(temperature.save)()

    async def close(self, code=None):
        print("Connection Closed ", code)


class DashboardConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        print("Connected .... ")
        await self.accept()
        await self.send_json({'message': 'Connected'})

    async def receive_json(self, content, **kwargs):
        async def get_objects():
            data = Temperature.objects.all()
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
