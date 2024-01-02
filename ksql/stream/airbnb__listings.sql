CREATE STREAM airbnb_raw__listings WITH (
    kafka_topic = 'airbnb.airbnb_raw.listings',
    value_format = 'avro',
    partitions=1
);

CREATE STREAM agg_airbnb_raw__listings 
WITH (
    kafka_topic = 'agg_airbnb_raw__listings',
    value_format='avro',
    partitions=2
) AS
    SELECT 
    listing_neighbourhood,
    SUM(CAST(price AS BIGINT)) AS price
    FROM airbnb_raw__listings
    GROUP BY listing_neighbourhood;