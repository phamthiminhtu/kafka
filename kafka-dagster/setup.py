from setuptools import find_packages, setup

setup(
    name="kafka_dagster",
    packages=find_packages(exclude=["kafka_dagster_tests"]),
    install_requires=[
        "dagster",
        "dagster-cloud",
        "dagster-gcp",
        "dagster-gcp-pandas"
        "google-auth-oauthlib"
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
