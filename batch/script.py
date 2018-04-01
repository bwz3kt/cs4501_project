from kafka import KafkaProducer
from elasticsearch import Elasticsearch
from kafka import KafkaConsumer
import time
import json

time.sleep(30)
consumer = KafkaConsumer('new-listings-topic', group_id='listing-indexer', bootstrap_servers=['kafka:9092'])
es = Elasticsearch(['es'])

print("Batch script running")
for message in consumer:
	listing = json.loads((message.value).decode('utf-8'))
	es.index(index='listing_index', doc_type='listing', id=listing['id'], body=listing)
	es.indices.refresh(index="listing_index")