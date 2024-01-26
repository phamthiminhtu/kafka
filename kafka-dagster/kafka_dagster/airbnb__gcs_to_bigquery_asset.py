from dagster_gcp import BigQueryResource
from dagster_gcp.gcs import GCSResource
from dagster import asset
from dagster import Definitions


GCP_PROJECT = 'kafka-408805'
BIGQUERY_DATASET = 'airbnb'
GCS_BUCKET = "kafka_airbnb"
GCS_BLOB_PREFIX = "topics/"

def create_bigquery_external_table(
        context,
        table_id,
        source_uris,
        bigquery_resource: BigQueryResource,
        external_source_format='CSV'
) -> None:
    from google.cloud import bigquery
    with bigquery_resource.get_client() as bq_client:
        context.log.info(f'Creating table {table_id}...')
        external_config = bigquery.ExternalConfig(external_source_format)
        external_config.source_uris = source_uris 
        table = bigquery.Table(table_id)
        table.external_data_configuration = external_config
        bq_client.create_table(table)
        context.log.info(f'Finish creating table {table_id}.')

def get_bigquery_tables(
        context,
        bq_project,
        bq_dataset,
        bigquery_resource: BigQueryResource,
        condition = "TRUE"
    ) -> list:
    context.log.info('Getting a list of existing external tables...')
    with bigquery_resource.get_client() as client:
        query = f"""
                    SELECT
                        table_catalog || "." || table_schema || "." || table_name AS table_id
                    FROM {bq_project}.{bq_dataset}.INFORMATION_SCHEMA.TABLES
                    WHERE {condition}
                """
        context.log.info(f'{query}')
        query_job = client.query(query)
        rows = query_job.result()
        context.log.info('Done getting a list of existing external tables.')
    return list(rows)

@asset
def get_bigquery_existing_external_tables(
        context,
        bigquery_resource: BigQueryResource,
    ) -> list:
    bq_tables_info = get_bigquery_tables(
        context,
        bq_project=GCP_PROJECT,
        bq_dataset=BIGQUERY_DATASET,
        bigquery_resource=bigquery_resource,
        condition = "table_type = 'EXTERNAL'"
    )
    existed_external_tables = [row[0] for row in bq_tables_info]
    return existed_external_tables

@asset
def get_gcs_blob(
        context,
        gcs_resource: GCSResource,
    ):
    gsc_client = gcs_resource.get_client()
    blobs = gsc_client.list_blobs(GCS_BUCKET, prefix=GCS_BLOB_PREFIX, delimiter='/')
    # Note: The call returns a response only when the iterator is consumed. https://cloud.google.com/storage/docs/listing-objects#client-libraries
    for blob in blobs:
        print(blob.name)
    context.log.info(f'{len(blobs.prefixes)} blobs found')
    return blobs.prefixes


@asset
def get_new_tables_to_create(
        context,
        get_bigquery_existing_external_tables,
        get_gcs_blob,
        gcs_resource: GCSResource,
    ) -> list:
    tables_to_create = []
    for blob_prefix in get_gcs_blob:
        topic = blob_prefix.split('/')[1]
        table_name = topic.split('.')[-1]
        table_id = f"{GCP_PROJECT}.{BIGQUERY_DATASET}.{table_name}"
        if table_id in get_bigquery_existing_external_tables:
            continue
        table_info = {
            "topic" : blob_prefix,
            "table_id" : table_id
        }
        tables_to_create.append(table_info)

    context.log.info(f'Total {len(tables_to_create)} new topics found. Tables to create:')
    context.log.info(tables_to_create)
    return tables_to_create

@asset
def bigquery_external_table_asset(
        context,
        get_bigquery_existing_external_tables,
        get_new_tables_to_create,
        bigquery_resource: BigQueryResource
    ) -> None:
    """
        Input: GCS location of files
        Output: External tables created on BigQuery
    """
    external_source_format = "AVRO"
    exceptions = []

    if len(get_new_tables_to_create) == 0:
        return
    for table_info in get_new_tables_to_create:
        source_uris = f'gs://kafka_airbnb/{table_info.get("topic")}*'
        table_id = table_info.get("table_id")
        try:
            create_bigquery_external_table(
                context,
                table_id=table_id,
                source_uris=source_uris,
                bigquery_resource=bigquery_resource,
                external_source_format=external_source_format
            )
        except Exception as e:
            exceptions.append(e)

    if exceptions:
        raise Exception(exceptions)


defs = Definitions(
    assets=[
        bigquery_external_table_asset,
        get_gcs_blob,
        get_new_tables_to_create,
        get_bigquery_existing_external_tables
    ],
    resources={
        "bigquery_resource": BigQueryResource(
            project=GCP_PROJECT
        ),
        "gcs_resource": GCSResource(
            project=GCP_PROJECT
        )
    }
)

