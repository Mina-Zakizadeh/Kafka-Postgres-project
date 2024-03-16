from kafka import KafkaConsumer
import json
import psycopg2

# Kafka configuration
source_topic = 'third_topic'
consumer_group = 'consumer-group'
bootstrap_servers = ['localhost:9092']

# PostgreSQL configuration
pg_host = 'postgres'
pg_port = '5432'
pg_user = 'postgres'
pg_password = 'postgres123'
pg_database = 'pg_kafka'
pg_table = 'user_data'

# Create Kafka consumer
consumer = KafkaConsumer(
    source_topic,
    group_id=consumer_group,
    bootstrap_servers=bootstrap_servers,
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    security_protocol='PLAINTEXT'
)

# Connect to PostgreSQL
conn = psycopg2.connect(
    host=pg_host,
    port=pg_port,
    user=pg_user,
    password=pg_password,
    database=pg_database
)
cur = conn.cursor()

# Consume messages from source topic and insert into PostgreSQL table
for message in consumer:
    data = message.value

    # Insert data into PostgreSQL table
    cur.execute(f'''
        INSERT INTO {pg_table} (first_name, last_name, gender, address, post_code, email, username, dob, registered_date, phone, picture, number)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ''', (
        data['first_name'], data['last_name'], data['gender'], data['address'], data['post_code'],
        data['email'], data['username'], data['dob'], data['registered_date'], data['phone'], data['picture'],
        data['number']
    ))
    conn.commit()

    print("Inserted data into PostgreSQL table")

# Close connections
consumer.close()
cur.close()
conn.close()