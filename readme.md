# Working with Docker, Postgres SQL, Ubuntu and Kafka altogether

In this repository I want to use docker as a medium to run postgres, unbuntu and kafka. The steps of this project is in the following steps:

1. Building a container in docker which has postgres sql, ubuntu and kafka (in the kafka we add there topics)

2. Getting random data from 'randomuser.me' by producer of first topic in kafka

3. Assigning new column as timestamp to dataset by consumer of first topic

4. Using the data of first topic in consumer of second topic and add another column as length of name and send them to third topic by the second topic producer

5. In the third topic we have just consumer for storing data in postgres sql database

6. Defining full backup of postgres sql

   ## 1. Defining a docker container

   In order to have access between ubuntu, postgres sql and kafka we should define them in a one container. In the docker_compose file I put the configuration of this container and for running it after you make sure that docker works well in command line or power shell in windows you should navigate to the path that your docker_compose exists and write the following command:

   ```powershell
   docker-compose -f .\docker_compose.yml up
   ```

   

> [!WARNING]
>
> Because we define a folder for postgres sql and kafka in container, make sure you created them in that folder.

After defining a docker container if you didn't downloaded images before it takes a little time to download all of requirements.

## 2. Defining kafka topics in ubuntu

In the ubuntu bash  we define there topics and get data by first one then add a timestamp column by consumer. In the second topic, consumer uses the updated data and adds another column which is the length of name of users and by producer sends it to the third topic. In the third topic we just insert each input data into pre-defined table.

Firstly, we define topics in kafka bash:

```bash
kafka-topics --bootstrap-server localhost:29092 --create --topic first_topic
kafka-topics --bootstrap-server localhost:29092 --create --topic second_topic
kafka-topics --bootstrap-server localhost:29092 --create --topic third_topic
```

Then we produce data from 'randomuser.me' using producer_1.py and cron by setting 1 min. In consumer_1.py we add a column .

In the consumer_producer2.py, we add an extra column and push it to next topic.

In consumer_3.py we store data in postgres sql with related configuration.

## 3. Defining postgres sql dataset

Before pushing the third topic in kafka to the dataset we should initialize it first, so in the pg_data folder in 'user.sql' is the sql file that we use to create appropriate database and table. For this purpose we can go to the postgres bash by following command:

```bash
docker exec -it YOUR_POSTGRES_ID bash
```

then we should go to the postgres user and go to psql mode then add sql file to run: 

```bash
su postgres
psql
\i /YOUR_SQL_PATH.sql
```



## 4. Performing full backup of postgres

For storing data and prevent of losing them we use backups. Full backup prevent losing data and uses the more efficient backup than other ways. Here we explain how can get backup of the postgres sql. In this backup we use this command on postgres container to store dataset from a specific date:

```bash
docker exec -it postgressql bash
su postgres
pg_basebackup -D /backup/standalone-"$(date +%Y-%m-%dT%H-%M)" -c fast -P -R 
```

After executing above commands a backup of database will store in backup folder as we set its direction. In db_data folder where our postgres configuration consists, we should modify postgresql.conf file as following:

- archive_mode = on
- archive_command = ' test ! -f /archive/%f && cp %p /archive/%f'
- wal_level = replica

After this configuration if there is any modifying on database, and some modification wasn't desirable and by following steps we can back to the database that we stored before:

- copy all files in standalone folder and paste them in root folder of dataset (here it is db_data)
- rename standby.signal file into recovery.signal
- we should modify postgresql.conf again as before mentioned plus following: restore_command = 'cp /archive/%f %p' and recovery_target_time = 'TIME_AND_DATE' and recovery_target_action = 'promote' 

> [!NOTE]
>
> The value of recovery_target_time should set to time and date just before unwanted modification

