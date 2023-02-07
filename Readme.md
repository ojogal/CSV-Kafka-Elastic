## Installation
### Install OpenJDK
```
sudo apt-get update
sudo apt-get install openjdk-8-jdk
```
### ElasticSearch
Download ES from [this link](https://www.elastic.co/downloads/past-releases/elasticsearch-5-3-2) and copy its contents to `./packages/elasticsearch`

### Apache Kafka
Download Kafka from [this link](https://www.apache.org/dyn/closer.cgi?path=/kafka/3.1.0/kafka_2.13-3.1.0.tgz) and copy its contents to `./packages/kafka`
***

### Install python libs
Smth like this:
```
sudo python3 -m pip install -r requirements.txt
```
## Startup

### Run elasticsearch
```
./packages/elasticsearch/bin/elasticsearch
```

### Run Kafka & Zookeeper daemons
Run in separate terminals:
```
./packages/kafka/bin/zookeeper-server-start.sh ./packages/kafka/config/zookeeper.properties
```

```
./packages/kafka/bin/kafka-server-start.sh ./packages/kafka/config/server.properties
```
