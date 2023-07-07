import asyncio

import aio_pika
from fastapi import FastAPI
from starlette.requests import Request

from config import RABBITMQ_HOST
# from auth_pb2_grpc import GetUserServiceStub
from src.delivery.router import router as delivery_router
from src.rabbitmq_consumer.consumer import consumer,loop
from src.rabbitmq_consumer.consumer import Consumer


app = FastAPI()


app.include_router(delivery_router)



@app.on_event('startup')
async  def startup_event_consumer():
    rabbitmq_connection = await aio_pika.connect_robust(
        loop=loop,
        url=f"amqp://{RABBITMQ_HOST}"
    )
    async with rabbitmq_connection.channel() as channel:
        await channel.set_qos(prefetch_count=100)
        await consumer.prepare_consumed_queue(channel)
        await consumer.start_consuming()
@app.on_event("shutdown")
async def shutdown_event():
    loop.close()
    await consumer.stop_consuming()
