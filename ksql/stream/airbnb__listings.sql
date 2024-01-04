CREATE OR REPLACE STREAM stream__listings
WITH (KAFKA_TOPIC='airbnb.airbnb_raw.listings', VALUE_FORMAT='AVRO');

CREATE OR REPLACE STREAM stream__listings_copy (listing_id BIGINT, scrape_id VARCHAR)
  WITH (KAFKA_TOPIC='airbnb.airbnb_raw.listings_copy',
        VALUE_FORMAT='AVRO');

CREATE OR REPLACE TABLE table_listings AS
SELECT
    listing_id,
    COUNT(*)
FROM stream__listings_copy
GROUP BY listing_id
EMIT CHANGES;

CREATE OR REPLACE STREAM agg_airbnb_raw__listings 
WITH (
    kafka_topic = 'agg_airbnb_raw__listings',
    value_format='avro',
    partitions=2
) AS
    SELECT 
        listing_id, 
        scrape_id
    FROM stream__listings
    EMIT CHANGES;



CREATE STREAM customers_by_key AS
    