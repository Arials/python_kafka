from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer
import time
import random

# Define the Avro schema we want our produced records to conform to.
value_schema_str = """
{
  "namespace": "cratedb.metrics",
  "name": "value",
  "type": "record",
  "fields": [
    {"name": "id", "type": "string"},
    {"name": "timestamp", "type": "int"},
    {"name": "temperature", "type": "float"},
    {"name": "humidity", "type": "float"},
    {"name": "pressure", "type": "float"},
    {"name": "luminosity", "type": "float"}
  ]
}
"""

# Load the Avro schema.
value_schema = avro.loads(value_schema_str)

# Create an Avro producer using the defined schema, assuming that our
# Kafka servers are running at localhost:9092 and the Schema Registry
# server is running at localhost:8081.
avroProducer = AvroProducer(
    {
        "bootstrap.servers": "172.20.10.3:9092",
        "schema.registry.url": "http://172.20.10.3:8081",
    },
    default_value_schema=value_schema,
)

# Create a metric payload from a simulated sensor device.
def create_metric():
    sensor_id = "sensor-" + str(random.choice(list(range(1, 21))))
    temperature = random.uniform(-5, 35)
    humidity = random.uniform(0, 100)
    pressure = random.uniform(1000, 1030)
    luminosity = random.uniform(0, 65000)
    timestamp = int(time.time())
    return {
        "id": sensor_id,
        "timestamp": timestamp,
        "temperature": temperature,
        "humidity": humidity,
        "pressure": pressure,
        "luminosity": luminosity,
        "timestamp": timestamp,
    }


# Create a new metric every 0.25 seconds and push it to the metrics topic.
while True:
    value = create_metric()
    avroProducer.produce(topic="metrics", value=value)
    avroProducer.flush()
    time.sleep(0.25)