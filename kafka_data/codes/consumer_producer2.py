from kafka import KafkaConsumer, KafkaProducer
import json

# Kafka configuration
source_topic = 'second_topic'
destination_topic = 'third_topic'
consumer_group = 'consumer-group'
bootstrap_servers = ['localhost:9092']

# Create Kafka consumer
consumer = KafkaConsumer(
    source_topic,
    group_id=consumer_group,
    bootstrap_servers=bootstrap_servers,
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    security_protocol='PLAINTEXT'
)

# Create Kafka producer
producer = KafkaProducer(
    bootstrap_servers=bootstrap_servers,
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    security_protocol='PLAINTEXT'
)

# Consume messages from source topic, add number column, and produce to destination topic
for message in consumer:
    data = message.value
    number = len(data['first_name'])  # Example: Add number column based on length of email
    data['number'] = number  # Add number column to the data

    # Print received message and modified data
    print(f"Received message: {data} | Added number: {number}")

    # Produce modified data to the destination topic
    producer.send(destination_topic, value=data)

# Close Kafka connections
consumer.close()
producer.close()
