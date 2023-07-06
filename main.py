import asyncio

import aio_pika
from fastapi import FastAPI
from starlette.requests import Request
# from auth_pb2_grpc import GetUserServiceStub
from src.delivery.router import router as delivery_router
from src.rabbitmq_consumer.consumer import consumer,loop
from src.rabbitmq_consumer.consumer import Consumer


app = FastAPI()


app.include_router(delivery_router)



@app.on_event("startup")
async def startup_event():
    rabbitmq_connection = await aio_pika.connect_robust(
        loop=loop,
        url="amqp://guest:guest@localhost/"
    )

    async with rabbitmq_connection.channel() as channel:
        await channel.set_qos(prefetch_count=100)
        await consumer.prepare_consumed_queue(channel)
        await consumer.start()

@app.on_event("shutdown")
async def shutdown_event():
    loop.close()
    await consumer.stop()
