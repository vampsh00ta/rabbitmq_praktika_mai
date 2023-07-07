import json

import aio_pika
from aio_pika import Queue, IncomingMessage, Connection, Message
import asyncio
from config import RABBITMQ_CONN, RABBITMQ_EXCHANGE_NAME

loop = asyncio.get_event_loop()



def singleton(cls):
    instances = {}
    def wrapper(*args, **kwargs):
        if cls not in instances:
          instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return wrapper


@singleton
class Producer():
    def __init__(self):
        self.channel = None
        self.exchange = None
    async def start(self,connection,*queues):
        self.channel = await connection.channel()
        self.exchange = await self.channel.declare_exchange(name=RABBITMQ_EXCHANGE_NAME)
        for queue_name in queues:
            queue = await self.channel.declare_queue(name=queue_name,auto_delete=True)
            await queue.bind(self.exchange,queue_name)

    async def convert_dict_to_bytes(self,data:dict)->Message:
        converted_data = json.dumps(data).encode()
        return  aio_pika.Message(converted_data)
    async def send_default(self,data:dict,key:str):
        data = await self.convert_dict_to_bytes(data)
        await self.exchange.publish(message =data,routing_key=key)

producer = Producer()
