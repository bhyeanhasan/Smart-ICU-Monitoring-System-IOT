from channels.generic.websocket import AsyncJsonWebsocketConsumer
from .models import Temperature
from channels.db import database_sync_to_async


class TemperatureConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        print("Connected .... ")
        await self.accept()
        await self.send_json({'message': 'Connected'})

    async def receive_json(self, content, **kwargs):
        patient_temperature = content['temperature']
        time = content['time']
        print(patient_temperature)
        temperature = Temperature()
        temperature.patient_temp = patient_temperature
        temperature.time = time
        await database_sync_to_async(temperature.save)()
        # await self.send_json({'message':'okay got it'})

    async def close(self, code=None):
        print("Connection Closed ", code)


class DashboardConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        print("Connected .... ")
        await self.accept()
        await self.send_json({'message': 'Connected'})

    async def receive_json(self, content, **kwargs):
        await self.send_json({'message': content['message']})

    async def close(self, code=None):
        print("Connection Closed ", code)
        await self.send_json({'message': 'Connection Closed'})
