import time
from venv import create
import requests
from kafka import KafkaProducer
from kafka.errors import KafkaError
from kafka.admin import KafkaAdminClient, NewTopic
import json
import os
import csv_to_json

config = json.loads(open('config.json', 'r').read())


admin = KafkaAdminClient(
    bootstrap_servers=config['kafka']['hostname'],
    client_id='admin'
)

def createTopic(topic_name):
    print('Actual topics:', admin.list_topics())
    if topic_name not in admin.list_topics():
        topic = NewTopic(name=topic_name,
                         num_partitions=1,
                         replication_factor=1)
        admin.create_topics(new_topics=[topic], validate_only=False)
        return True
    else:
        print(f"Topic `{topic_name}` already exists")

def dispatchEvent(topic_name, data):
    producer = KafkaProducer(bootstrap_servers=[config['kafka']['hostname']])
    future = producer.send(topic_name, data)
    try:
        future.get(timeout=10)
        print('Sent')
        return True
    except KafkaError as e:
        print('Error')
        return False

def getParsedCSV(src):
    csv_to_json.convert(src)
    parsed = json.loads(open(f"{src}.json", 'r').read())
    return parsed

createTopic(config['kafka']['topic'])

rows_to_send = getParsedCSV(config['source']['csv'])

for i in range(len(rows_to_send)):
    print(f"ROW {i+1}\t\tID {rows_to_send[i].get('ID')}\t\t STATUS ", end="")
    dispatchEvent(config['kafka']['topic'], bytes(
        json.dumps(rows_to_send[i]), 'utf-8'))
    time.sleep(2)
