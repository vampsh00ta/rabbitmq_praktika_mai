import asyncio

# from fastapi import Depends
from sqlalchemy import select
import smtplib

from utils.producer import producer
from worker import celery_app
from datetime import datetime
from src.authv2.models import Item, User
from utils.database import  async_session_maker


# celery_app.conf.beat_schedule = {
#     'check_expiring': {
#         'task': 'check_expiring',
#         "schedule": crontab(minute="*/0.5"),
#     },
# }


async def async_check_expiring():
    async with async_session_maker.begin() as session:
        items_query = select(Item).where(Item.expiring_at <= datetime.utcnow()).where(Item.is_active == True)
        items = (await session.execute(items_query)).scalars().all()
        if items:
            for item in items:
                user_id = item.owner_id
                item.is_active = False
                item.change_time = datetime.utcnow()
                session.add(item)
                user_query = select(User).where(User.id ==user_id)
                user = (await session.execute(user_query)).scalars().first()
                producer.send(KAFKA_TOPIC_EMAIL,{

                })
                task = email_sender.delay(user.email)
                return {"task_id": task.id}


@celery_app.task(name='email_sender')
def email_sender(email):
    email_sedner = 'lilopium@yahoo.com'
    password = 'ijgkifkiviopafbb'
    with smtplib.SMTP(host='smtp.mail.yahoo.com',port=587) as server:
        server.starttls()
        server.login(email_sedner, password)
        server.sendmail(email_sedner,email ,'ur item has been expired')


@celery_app.task(name='check_expiring')
def check_expiring():
    asyncio.run(async_check_expiring())



