from curses.ascii import ESC
from kafka import KafkaConsumer
from datetime import datetime
from elasticsearch import Elasticsearch
import time
import json
import sys
import requests

config = json.loads(open('config.json', 'r').read())

# ESClient = Elasticsearch(hosts=["http://localhost:9200"])
ESClient = Elasticsearch(cloud_id=config['elastic']['cloud_id'],
                         basic_auth=(config['elastic']['auth']['user'], config['elastic']['auth']['pass']))

# ESClient.indices.delete(index=config['kafka']['topic'])
# To consume messages
def transportMessages():
    consumer = KafkaConsumer(config['kafka']['topic'],
                             group_id="es_group",
                             auto_commit_interval_ms=30 * 1000,
                             auto_offset_reset='smallest',
                             bootstrap_servers=[config['kafka']['hostname']])
    esid = 0

    for message in consumer:
        esid = esid + 1
        msg = json.loads(message.value)
        print('Got new message', msg)

        resp = ESClient.index(
            index=config['kafka']['topic'], id=esid, document=msg)
        print(resp['result'])

transportMessages()

# Uncomment the code below to list entries by specified index

# def searchDocs(index):
#     res = ESClient.search(index=index, query={
#         'match_all': {}
#     })
#     return res


# selectedIndex = None
# while selectedIndex is None:
#     selectedIndex = input("Select index: ") or None
#     if selectedIndex is None:
#         continue
#     if not ESClient.indices.exists(index=selectedIndex):
#         print("Index does not exist\n")
#         selectedIndex = None
#         continue
#     else:
#         result = searchDocs(selectedIndex)
#         print(f"Loaded {result['_shards']['successful']} of {result['_shards']['total']}")
#         for entry in result['hits']['hits']:
#           print(entry['_source'])
