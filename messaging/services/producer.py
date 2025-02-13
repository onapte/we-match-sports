from kafka import KafkaProducer
import json
from ..config.kafka_settings import KAFKA_SERVERS, KAFKA_TOPIC_PREFIX


def create_new_producer(kafka_servers=KAFKA_SERVERS):
    return KafkaProducer(
        bootstrap_servers=kafka_servers,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

def send_message(producer, sender_id, recipient_id, message_content, kafka_topic_prefix=KAFKA_TOPIC_PREFIX):
    topic= f'{kafka_topic_prefix}-{recipient_id}'
    
    message = {
        'sender_id': sender_id,
        'recipient_id': recipient_id,
        'content': message_content
    }

    producer.send(topic, message)
    producer.flush()