from kafka import KafkaConsumer
import os
import json
from sqlalchemy import create_engine
from sqlalchemy.sql import text

TOPIC_NAME = 'locations'
KAFKA_CONSUMER_SERVER = 'kafka.default.svc.cluster.local:9092'

DB_USERNAME = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]

consumer = KafkaConsumer(TOPIC_NAME, bootstrap_servers=[KAFKA_CONSUMER_SERVER])

while True:
    for message in consumer:
        location = message.value.decode('utf-8')
        save_location(json.loads(location))

def save_location(location):
    person_id = int(location["person_id"])
    latitude = location["latitude"]
    longitude = location["longitude"]

    try:
        engine = create_engine(f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
        connect = engine.connect()
        sql = text("INSERT INTO location (person_id, coordinate) VALUES (:person_id, ST_Point(:latitude,:longitude))")
        connect.execute(sql, {"person_id": person_id, "latitude": latitude, "longitude": longitude})
    except:
        print('Insert error!')
