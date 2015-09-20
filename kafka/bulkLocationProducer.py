#!/usr/bin/python

# Kafka producer that reads the input data in a loop in order to simulate real time events
import csv
import json
import sys

from kafka import KafkaClient, SimpleProducer


class Producer():
    def __init__(self, topic, source_file):
        self.topic = topic
        self.source_file = source_file
        with open("../config/config.json", 'rb') as file:
            self.config = json.load(file)

    def genData(self):

        with open(self.source_file) as f:
            reader = csv.DictReader(f)
            crimeLocations = list(reader)

        kafka_cluster = self.config['kafka_cluster']
        kafka_client = KafkaClient(kafka_cluster)
        kafka_producer = SimpleProducer(kafka_client)

        count = 0
        while True:
            for loc in crimeLocations:
                print loc.keys()
                crimeId = loc["crime_id"]
                latitude = float(loc['latitude'])
                longitude = float(loc['longitude'])
                msg = {}
                msg['crime_id'] = crimeId
                location = {
                    'latitude': latitude,
                    'longitude': longitude
                }
                msg['location'] = location
                kafka_producer.send_messages(self.topic, json.dumps(msg))
                print "sending location update for crime %s" % crimeId
            count += 1
            print "+++++++++++++FINISH ROUND %d+++++++++++++++++" % count


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: [*.py] [source-file]"
        sys.exit(0)
        # logging.basicConfig(filename='error.log',level=logging.DEBUG)

    # logger = logging.getLogger('geo_app')
    # # create file handler which logs even debug messages
    # fh = logging.FileHandler('geoupdate.log')
    # fh.setLevel(logging.INFO)
    # logger.addHandler(fh)
    producer = Producer(
        topic='crimeLocation',
        source_file=sys.argv[1]
    )

    producer.genData()
