from kafka import KafkaProducer
from elasticsearch import Elasticsearch
from kafka import KafkaConsumer
import time
import json

print("Batch Script Running")
time.sleep(10)

consumer = KafkaConsumer('new-listings-topic', group_id='listing-indexer', bootstrap_servers=['kafka:9092'])
es = Elasticsearch(['es'])

fixtures = [{"name": "Apartment 1", "price": 750, "rating": "3.50", "username": "cyeung", "id": 1}, {"name": "Apartment 2", "price": 875, "rating": "2.95", "username": "cyeung", "id": 2},
            {"name": "Apartment 3", "price": 1925, "rating": "4.25", "username": "cyeung", "id": 3}, {"name": "Apartment 4", "price": 968, "rating": "4.95", "username": "tk9at", "id": 4},
            {"name": "Apartment 5", "price": 478, "rating": "3.81", "username": "tk9at", "id": 5}, {"name": "Apartment 6 ", "price": 899, "rating": "4.50", "username": "tk9at", "id": 6},
            {"name": "Apartment 7", "price": 2500, "rating": "1.50", "username": "bradyw7", "id": 7}, {"name": "Apartment 8", "price": 2384, "rating": "0.75", "username": "bradyw7", "id": 8}]
for apartment in fixtures:
    es.index(index='listing_index', doc_type='listing', id=apartment['id'], body=apartment)
    es.indices.refresh(index="listing_index")
print("Apartment Fixtures Loaded.")

# user_consumer = KafkaConsumer('user-listings-topic', group_id='listing-indexer', bootstrap_servers=['kafka:9092'])
users_fixtures = [{"username": "cyeung", "email": "cy4bv@virginia.edu"},
  {"username": "tk9at", "email": "tk9at@virginia.edu"},
  {"username": "bradyw7", "email": "bwz3kt@virginia.edu"}]

for user in users_fixtures:
    es.index(index='user_index', doc_type='listing', body=user)
    es.indices.refresh(index="user_index")
print("User Fixtures Loaded.")

for message in consumer:
    new_listing = json.loads((message.value).decode('utf-8'))[0]
    print(new_listing)
    if 'email' in new_listing:
        es.index(index='user_index', doc_type='listing', body=new_listing)
        es.indices.refresh(index="user_index")
    else:
        es.index(index='listing_index', doc_type='listing', id=new_listing['id'], body=new_listing)
        es.indices.refresh(index="listing_index")

# for message in user_consumer:
#     new_listing = json.loads((message.value).decode('utf-8'))[0]
#     print(new_listing)
#     es.index(index='user_index', doc_type='listing', body=new_listing)
#     es.indices.refresh(index="user_index")
#
