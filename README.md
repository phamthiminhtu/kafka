# run docker
docker-compose.yml up -d
# run new command in kafka container
docker exec -it kafka /bin/sh
# go to bin
cd opt/bitnami/kafka/bin


kafka-topics.sh --bootstrap-server localhost:9092 --describe --topic test

kafka-console-producer.sh --broker-list localhost:9092 --topic test

kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic test --from-beginning

Install Kafka Connectors in Docker:
- Doc: https://rmoff.net/2020/06/19/how-to-install-connector-plugins-in-kafka-connect/
- Currently using the 2nd way

Monitor Kafka connect and Connector
https://docs.confluent.io/platform/current/connect/monitoring.html 