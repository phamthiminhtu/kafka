FROM confluentinc/cp-kafka-connect-base:5.5.0

RUN confluent-hub install --no-prompt debezium/debezium-connector-postgresql:1.1.0 \
   && confluent-hub install --no-prompt wepay/kafka-connect-bigquery:2.5.2 \
   && confluent-hub install --no-prompt confluentinc/kafka-connect-gcp-bigtable:2.0.4