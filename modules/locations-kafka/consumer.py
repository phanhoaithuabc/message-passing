from kafka import KafkaConsumer

TOPIC_NAME = 'locations'
KAFKA_SERVER = 'kafka-headless:9092'

consumer = KafkaConsumer(TOPIC_NAME, bootstrap_servers=KAFKA_SERVER)
for message in consumer:
    print (message)

while True:
    msg_pack = consumer.poll(timeout_ms=500)
    for tp, messages in msg_pack.items():
        print ("%s:%d:%d: key=%s value=%s" % (tp.topic, tp.partition, message.offset, message.key, message.value))