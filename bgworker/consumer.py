import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.exchange_declare(exchange='whatsappbotevents', exchange_type='direct')  
channel.queue_declare( queue='payslip' )

def callback(ch, method, properties, body):
    print(" [x] Received %r %r" % (body,  method.routing_key))

channel.queue_bind( exchange='whatsappbotevents', 
    queue='payslip' ,routing_key='payslip_pdf_request')

channel.basic_consume( on_message_callback=callback,
                      queue='payslip',
                        auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
