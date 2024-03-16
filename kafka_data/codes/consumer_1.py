from kafka import KafkaConsumer
import json
from datetime import datetime

# Kafka configuration
source_topic = 'first_topic'
bootstrap_servers = ['localhost:9092']

# Create Kafka consumer
consumer = KafkaConsumer(
    source_topic,
     group_id='my-group1'
    bootstrap_servers=bootstrap_servers,
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    security_protocol='PLAINTEXT'
)

# Consume messages from source topic and add timestamp
for message in consumer:
    data = message.value
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Get current timestamp
    data['timestamp'] = timestamp  # Add timestamp to the data

    print(f"Received message with timestamp '{timestamp}': {data}")

    # Perform any additional processing as needed
    
# Close Kafka connection
consumer.close()