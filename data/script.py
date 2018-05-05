from kafka import KafkaProducer
from kafka import KafkaConsumer
import time
import json
import os

print("Spark Script Running.")
time.sleep(40)

consumer = KafkaConsumer('spark-topic', group_id='listing-indexer', bootstrap_servers=['kafka:9092'])


for message in consumer:
    new_listing = json.loads((message.value).decode('utf-8'))[0]
    print(new_listing)
    with open("/tmp/data/access.log", 'a') as file:
        file.write(str(new_listing['user_id']) + ' ' + str(new_listing['id']) + '\n')