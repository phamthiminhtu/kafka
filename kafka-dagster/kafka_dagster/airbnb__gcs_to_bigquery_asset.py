import pandas as pd
from dagster_gcp import BigQueryResource
from dagster_gcp.gcs import GCSResource
from google.cloud import bigquery

from dagster import Definitions, SourceAsset, asset, EnvVar, op

GCP_PROJECT = 'kafka-408805'
BIGQUERY_DATASET = 'airbnb'
GCS_BUCKET = "kafka_airbnb"
GCS_BLOB_PREFIX = "topics/"


@asset
def create_external_table(
        context,
        bigquery_resource: BigQueryResource,
        gcs_resource: GCSResource,
    ) -> None:
    """
        Input: GCS location of files
        Output: External tables created on BigQuery
    """
    gsc_client = gcs_resource.get_client()
    blobs = gsc_client.list_blobs(GCS_BUCKET, prefix=GCS_BLOB_PREFIX, delimiter='/')
    external_source_format = "AVRO"

    exceptions = []
    # Note: The call returns a response only when the iterator is consumed. https://cloud.google.com/storage/docs/listing-objects#client-libraries
    for blob in blobs:
        print(blob.name)
    context.log.info(f'{len(blobs.prefixes)} topics found.')
    context.log.info(blobs.prefixes)
    for blob_prefix in blobs.prefixes:
        topic = blob_prefix.split('/')[1]
        table_name = topic.split('.')[-1]
        table_id = f"{GCP_PROJECT}.{BIGQUERY_DATASET}.{table_name}"

        try:
            with bigquery_resource.get_client() as bq_client:
                is_created = None
                try:
                    is_created = bq_client.get_table(table_id)
                except Exception:
                    pass
                if is_created:
                    context.log.info(f'Table {table_id} already exists.')
                    continue
                else:
                    context.log.info(f'Creating table {table_id}...')
                    external_config = bigquery.ExternalConfig(external_source_format)
                    external_config.source_uris = f'gs://kafka_airbnb/{blob_prefix}*'
                    table = bigquery.Table(table_id)
                    table.external_data_configuration = external_config
                    bq_client.create_table(table)
        except Exception as e:
            exceptions.append(e)

    if exceptions:
        raise Exception(exceptions)




