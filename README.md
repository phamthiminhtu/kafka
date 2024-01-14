# Description
Streaming data with Kafka. Current projects:
- CDC (change data capture): stream data from Postgres database to GCP Bigtable using Debezium (log-based Kafka CDC) and Kafka Connect provided by Confluent Platform

# Useful resources

Install Kafka Connectors in Docker:
- Doc: https://rmoff.net/2020/06/19/how-to-install-connector-plugins-in-kafka-connect/

Monitor Kafka connect and Connector
https://docs.confluent.io/platform/current/connect/monitoring.html 

Stream ELT pipeline
https://docs.ksqldb.io/en/latest/tutorials/etl/?_ga=2.12145522.779215627.1700084765-1437246833.1700084765#create-the-ksqldb-source-streams

KSQL
docker exec -it ksqldb-cli ksql http://ksqldb-server:8088

Start the connector
curl -i -X POST -H "Accept:application/json" -H  "Content-Type:application/json" http://localhost:8083/connectors/ -d @opt/connectors/sink/gcp/gcs-sink.json

CICD with CloudBuild, Compute Engine
https://beranger.medium.com/automate-deployment-with-google-compute-engine-and-cloud-build-cccd5c3eb93c

Generate SSH 
https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent?platform=linux


