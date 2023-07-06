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
            # await self.channel.queue_bind(exchange=RABBITMQ_EXCHANGE_NAME,queue=queue)

    async def convert_dict_to_bytes(self,data:dict)->Message:
        converted_data = json.dumps(data).encode()
        return  aio_pika.Message(converted_data)
    async def send_default(self,data:dict,key:str):
        data = await self.convert_dict_to_bytes(data)
        await self.exchange.publish(message =data,routing_key=key)

producer = Producer()
# class Consumer():
#     def __init__(self,queue:Queue,
#                  iterator_timeout:int = 5,
#                  iterator_timeout_sleep: float = 5.0,
#                  *args,
#                  **kwargs):
#         self.queue = queue
#         self.iterator_timeout = iterator_timeout
#         self.iterator_timeout_sleep = iterator_timeout_sleep
#         self.consuming_flag = True
#
#     async def consume(self ):
#         async with self.queue.iterator(timeout=self.iterator_timeout) as queue_iterator:
#             while self.consuming_flag:
#                 try:
#                     async for message in queue_iterator:
#                         await self.process_message(message)
#                         if not self.consuming_flag:
#                             break
#                 except asyncio.exceptions.TimeoutError:
#                     await self.on_finish()
#                     if self.consuming_flag:
#                         await asyncio.sleep(self.iterator_timeout_sleep)
#
#     async def on_finish(self):
#         pass
#     def stop_consuming(self):
#         self.consuming_flag = False
#     async def process_message(self, orig_message: IncomingMessage):
#         raise NotImplementedError()