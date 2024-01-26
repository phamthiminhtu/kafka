# Description
Streaming data with Kafka. Current projects:
## CDC (change data capture)
![kafka](https://github.com/phamthiminhtu/kafka/assets/56192840/e0e116dc-bdf3-40ce-b39d-11bb87609f40)

The workflow is as follows:
  1. Stream data from Postgres to Kakfa using Debezium (log-based CDC), KSQL and Kafka Connect provided Confluent Platform. Code: [ksql/sink/sink__bigquery__airbnb.sql](https://github.com/phamthiminhtu/kafka/blob/master/ksql/source/source__postgres__airbnb.sql)
  2. Sink data from Kafka to Google Cloud Storage using Kafka Connect. Code: [connectors/sink/gcp/gcs-sink.json](https://github.com/phamthiminhtu/kafka/blob/master/connectors/sink/gcp/gcs-sink.json)
  3. Automatically detect and create new topics as tables on BigQuery using Dagster. Code: [kafka-dagster/kafka_dagster/airbnb__gcs_to_bigquery_asset.py](https://github.com/phamthiminhtu/kafka/blob/master/kafka-dagster/kafka_dagster/airbnb__gcs_to_bigquery_asset.py)
  - Example of the DAG created on Dagster:
<img width="1425" alt="image" src="https://github.com/phamthiminhtu/kafka/assets/56192840/88b56648-cd19-4c0c-9911-5324a3c68a34">


# Useful resources

- Install Kafka Connectors in Docker:
  Doc: https://rmoff.net/2020/06/19/how-to-install-connector-plugins-in-kafka-connect/

- Monitor Kafka connect and Connector
https://docs.confluent.io/platform/current/connect/monitoring.html 

- Stream ELT pipeline
https://docs.ksqldb.io/en/latest/tutorials/etl/?_ga=2.12145522.779215627.1700084765-1437246833.1700084765#create-the-ksqldb-source-streams

- KSQL
docker exec -it ksqldb-cli ksql http://ksqldb-server:8088

- Create a connector
curl -i -X POST -H "Accept:application/json" -H  "Content-Type:application/json" http://localhost:8083/connectors/ -d @opt/connectors/sink/gcp/gcs-sink.json

- Update the connector 
(the config file structure is a little bit different from POST [ref](https://stackoverflow.com/questions/53384144/kafka-connect-rest-interface-put-connectors-string-name-config-return-erro)
)
curl --request PUT -H "Accept:application/json" -H  "Content-Type:application/json" http://localhost:8083/connectors/gcs-sink/config -d @opt/connectors/sink/gcp/archive/gcs-sink-update.json

- List current connectors
curl --request GET -H "Accept:application/json" -H  "Content-Type:application/json" http://localhost:8083/connectors/

- CICD with CloudBuild, Compute Engine
https://beranger.medium.com/automate-deployment-with-google-compute-engine-and-cloud-build-cccd5c3eb93c

- Generate SSH 
https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent?platform=linux

- Docker build
docker build --tag tototus-dagster --file Dockerfile-dagster .


