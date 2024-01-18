from dagster import Definitions, load_assets_from_modules
from dagster_gcp import BigQueryResource
from dagster_gcp.gcs import GCSResource
from . import airbnb__gcs_to_bigquery_asset

GCP_PROJECT = 'kafka-408805'
BIGQUERY_DATASET = 'airbnb'
GCS_BUCKET = "kafka_airbnb"
GCS_BLOB_PREFIX = "topics/"

all_assets = load_assets_from_modules([airbnb__gcs_to_bigquery_asset])

defs = Definitions(
    assets=all_assets,
    resources={
        "bigquery_resource": BigQueryResource(
            project=GCP_PROJECT
        ),
        "gcs_resource": GCSResource(
            project=GCP_PROJECT
        )
    }
)
