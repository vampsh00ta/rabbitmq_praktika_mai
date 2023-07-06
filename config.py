import smtplib

import aioredis
from dotenv import load_dotenv
import os
import logging
load_dotenv()

DB_NAME=os.environ.get('DB_NAME')
DB_USER=os.environ.get('DB_USER')
DB_PASSWORD=os.environ.get('DB_PASSWORD')
DB_HOST=os.environ.get('DB_HOST')
DB_PORT=os.environ.get('DB_PORT')
SECRET=os.environ.get('SECRET')
REDIS_URL = os.environ.get('REDIS_URL')
KAFKA_TOPIC = os.getenv('KAFKA_TOPIC')
KAFKA_CONSUMER_GROUP = os.getenv('KAFKA_CONSUMER_GROUP', 'group')
KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
KAFKA_TOPIC_RECOMMENDATIONS = os.getenv('KAFKA_TOPIC_RECOMMENDATIONS')
KAFKA_TOPIC_DELIVERY = os.getenv('KAFKA_TOPIC_DELIVERY')


#logger
logger = logging.getLogger(__name__)
rabbitmq_handler = logging.StreamHandler()
rabbitmq_format =logging.basicConfig(format='%(levelname)s:      RABBITMQ:%(name)s - %(message)s')
rabbitmq_handler.setFormatter(rabbitmq_format)
logger.setLevel(logging.INFO)
logging.root.setLevel(logging.NOTSET)
logger.addHandler(rabbitmq_handler)




#rabbitmq
RABBITMQ_DEAD_LETTER_EXCHANGE_NAME=os.getenv('RABBITMQ_DEAD_LETTER_EXCHANGE_NAME')
RABBITMQ_QUEUE_NAME = os.getenv('RABBITMQ_QUEUE_NAME')
RABBITMQ_EXCHANGE_NAME = os.getenv('RABBITMQ_EXCHANGE_NAME')
DEFAULT_QUEUE_PARAMETERS = {
    "auto_delete":True

}


