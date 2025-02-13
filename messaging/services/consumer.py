from kafka import KafkaConsumer
from kafka.structs import TopicPartition
from ..config.kafka_settings import KAFKA_SERVERS, KAFKA_TOPIC_PREFIX
import json


def receive_message(user_id):
    topic = f'{KAFKA_TOPIC_PREFIX}-{user_id}'

    consumer = KafkaConsumer(
        bootstrap_servers=KAFKA_SERVERS,
        value_deserializer=lambda v: json.loads(v.decode('utf-8')),
        consumer_timeout_ms=1000,
    )

    partition = TopicPartition(topic, 0)
    consumer.assign([partition])
    end_offset = consumer.end_offsets([partition])

    last_offset = list(end_offset.values())[0]

    if last_offset == 0:
        print("No messages in topic.")
        consumer.close()
        return None

    consumer.seek(partition, last_offset - 1)

    last_message = None
    for message in consumer:
        last_message = message.value
        break

    consumer.close()
    return last_message