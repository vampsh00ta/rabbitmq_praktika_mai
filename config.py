import smtplib

import aioredis
import logging

from dotenv import load_dotenv
import os
load_dotenv()




DB_NAME=os.environ.get('DB_NAME')
DB_USER=os.environ.get('DB_USER')
DB_PASSWORD=os.environ.get('DB_PASSWORD')
DB_HOST=os.environ.get('DB_HOST')
DB_PORT=os.environ.get('DB_PORT')
SECRET=os.environ.get('SECRET')
JWT_LIFE=int(os.environ.get('JWT_LIFE'))
REDIS_URL = os.environ.get('REDIS_URL')
RABBITMQ_CONN=os.environ.get('RABBITMQ_CONN')
RABBITMQ_QUEUE_KEY_EMAIL=os.environ.get('RABBITMQ_QUEUE_KEY_EMAIL')
RABBITMQ_QUEUE_KEY_RECOMMENDATIONS=os.environ.get('RABBITMQ_QUEUE_KEY_RECOMMENDATIONS')
RABBITMQ_QUEUE_KEY_DELIVERY=os.environ.get('RABBITMQ_QUEUE_KEY_DELIVERY')
RABBITMQ_EXCHANGE_NAME=os.environ.get('RABBITMQ_EXCHANGE_NAME')

