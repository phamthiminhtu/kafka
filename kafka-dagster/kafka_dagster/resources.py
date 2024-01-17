from dagster import EnvVar, Definitions, ConfigurableResource

# This launches a local server to be used as the callback URL in the desktop
# app auth flow. If you are accessing the application remotely, such as over
# SSH or a remote Jupyter notebook, this flow will not work. Use the
# `gcloud auth application-default login --no-browser` command or workload
# identity federation to get authentication tokens, instead.
#
appflow.run_local_server()

credentials = appflow.credentials

class BigQuerysResource(ConfigurableResource):
    username: str
    password: str
