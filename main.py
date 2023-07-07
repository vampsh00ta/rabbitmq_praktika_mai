import asyncio

import aio_pika
from fastapi import FastAPI

from config import RABBITMQ_QUEUE_KEY_EMAIL, RABBITMQ_QUEUE_KEY_DELIVERY, RABBITMQ_QUEUE_KEY_RECOMMENDATIONS, \
    RABBITMQ_HOST
from src.authv2.router  import router as authv2_router
from src.items.router  import router as items_router
from src.cart.router import router as cart_router
from fastapi.middleware.cors import CORSMiddleware


from utils.producer import producer

app = FastAPI(title='main')

app.include_router(authv2_router)
app.include_router(cart_router)
app.include_router(items_router)

origins = ["localhost:8000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,

    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event('startup')
async  def startup_event_producer():

    loop = asyncio.get_event_loop()
    rabbitmq_connection = await aio_pika.connect_robust(
        loop=loop,
        url=f"amqp://{RABBITMQ_HOST}"
    )


    await producer.start(rabbitmq_connection,
        RABBITMQ_QUEUE_KEY_EMAIL,
        RABBITMQ_QUEUE_KEY_RECOMMENDATIONS,
        RABBITMQ_QUEUE_KEY_DELIVERY)

