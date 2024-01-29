{% snapshot property_snapshot %}

{# Get vars from airflow #}
{% set model_params = get_vars_from_airflow() %}

{{ config(
  strategy="timestamp",
  updated_at="updated_at",
  unique_key="listing_id",
) }}

WITH
  source AS
    (SELECT
      *,
      ROW_NUMBER() OVER(PARTITION BY listing_id ORDER BY scraped_date DESC) AS _row_number
    FROM {{ source('airbnb_raw', 'listings') }}
    -- only run 1 date of data to backfill data in the past
    WHERE scraped_date = DATE('{{ model_params.ds_date }}')
    )

  SELECT
    listing_id,
    listing_neighbourhood,
    property_type,
    room_type,
    accommodates,
    CAST(scraped_date AS TIMESTAMP) AS updated_at
  FROM source
  -- get the one unique record in case the unique key has different values within 1 scraped_date
  -- e.g.: 1 listing_id attached with 2 listing_neighbourhoods
  WHERE _row_number = 1
{% endsnapshot %}