
CREATE DATABASE pg_kafka;

CREATE TABLE IF NOT EXISTS user_data (
    id SERIAL PRIMARY KEY,
	first_name VARCHAR(255),
	last_name VARCHAR(255),
	gender VARCHAR(10),
	address TEXT,
	post_code VARCHAR(20),
	email VARCHAR(255),
	username VARCHAR(100),
	dob TIMESTAMP,
	registered_date TIMESTAMP,
	phone VARCHAR(50),
	picture VARCHAR(255),
	number INT
);