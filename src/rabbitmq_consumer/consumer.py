import asyncio
import json


from aio_pika import Channel
from sqlalchemy.ext.asyncio import AsyncSession

from config import DEFAULT_QUEUE_PARAMETERS, RABBITMQ_QUEUE_NAME, RABBITMQ_EXCHANGE_NAME


from src.rabbitmq_consumer.utils import singleton
from aio_pika.queue import Queue
from aio_pika.message import IncomingMessage
from src.rabbitmq_consumer.router import DeliveryRouter
from utils.database import get_async_session, async_session_maker

loop = asyncio.get_event_loop()


@singleton
class Consumer(DeliveryRouter):

    def __init__(
        self,
        get_session,
        iterator_timeout: int = 5,
        iterator_timeout_sleep: float = 5.0,

    ):
        self.get_session = get_session
        self.iterator_timeout = iterator_timeout
        self.iterator_timeout_sleep = iterator_timeout_sleep
        self.consuming_flag = True

    async def start(self):
        async with self.queue.iterator(timeout=self.iterator_timeout) as queue_iterator:
            while self.consuming_flag:
                try:
                    async for message in queue_iterator:
                        await self.process_message(message)
                        if not self.consuming_flag:
                            break
                except asyncio.exceptions.TimeoutError:
                    await self.on_finish()
                    if self.consuming_flag:
                        await asyncio.sleep(self.iterator_timeout_sleep)
    def serializer(self,message:IncomingMessage):
        string_message = message.body.decode("utf-8")
        handled_message  =  json.loads(json.loads(string_message))
        return handled_message
    async def process_message(self, message: IncomingMessage):

        handled_message = self.serializer(message)
        await self.create_delivery(delivery_data=handled_message, get_session=self.get_session)
    async def  on_finish(self):
        pass
    async def prepare_consumed_queue(self,channel: Channel) -> Queue:

        queue = await channel.declare_queue(
            RABBITMQ_QUEUE_NAME,
            **DEFAULT_QUEUE_PARAMETERS

        )

        await queue.bind(RABBITMQ_EXCHANGE_NAME, RABBITMQ_QUEUE_NAME)

        self.queue = queue
    def stop_consuming(self):
        self.consuming_flag = False


consumer = Consumer(async_session_maker)
