import pika
from ..config import RABBITMQ_URL

def publismessage(que,key,message):
    connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_URL))
    channel = connection.channel()
    channel.exchange_declare(exchange='whatsappbotevents', exchange_type='direct') 
    channel.queue_declare( queue=que )
    channel.basic_publish(exchange='whatsappbotevents',routing_key=key,body=message)
    connection.close()
    print('published')