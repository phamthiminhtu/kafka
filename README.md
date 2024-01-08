# Description
Streaming data with Kafka. Current projects:
- CDC (change data capture): stream data from Postgres database to GCP Bigtable using Debezium (log-based Kafka CDC) and Kafka Connect provided by Confluent Platform

# Useful resources

Install Kafka Connectors in Docker:
- Doc: https://rmoff.net/2020/06/19/how-to-install-connector-plugins-in-kafka-connect/
- Currently using the 2nd way

Monitor Kafka connect and Connector
https://docs.confluent.io/platform/current/connect/monitoring.html 

Stream ELT pipeline
https://docs.ksqldb.io/en/latest/tutorials/etl/?_ga=2.12145522.779215627.1700084765-1437246833.1700084765#create-the-ksqldb-source-streams

KSQL
docker exec -it ksqldb-cli ksql http://ksqldb-server:8088

Start the connector
curl -i -X POST -H "Accept:application/json" -H  "Content-Type:application/json" http://localhost:8083/connectors/ -d @opt/sink_connectors/bigtable/airbnb.airbnb_raw.listings.json

curl -i -X POST -H "Accept:application/json" -H  "Content-Type:application/json" http://localhost:8083/connectors/ -d @opt/sink_connectors/bigquery/airbnb.airbnb_raw.listings.json


