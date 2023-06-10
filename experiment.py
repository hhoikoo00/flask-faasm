"""
Module containing various webapps that are used in the experiments.
The apps are expected to be run with `gunicorn`. Configuration file in `./gunicorn.conf.py`.
It is also expected that the apps would be run on a 'production' level.

Usage:
* If Faasm processing should be disabled.
    * `gunicorn 'experiment:<create-func-name>()'`
* If Faasm processing should be enabled.
    * `gunicorn 'experiment:<create-func-name>(faasm=True)'`
"""


import logging

from flask import Flask

from lib.faasm import upload_cpython_runtime
from lib.flask import process_flask_app
from webapp import echo_app, pyperformance_app, simple_app

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def _create_app(app: Flask, use_faasm: bool = False, use_lib: bool = False) -> Flask:
    """Internal function for processing the given Flask `app`."""

    logger.info("Using Faasm!" if use_faasm else "Not using Faasm!")

    # Process the app if Faasm is used.
    if use_faasm:
        logger.info("Uploading CPython runtime...")
        upload_cpython_runtime()
        logger.info("Finished uploading CPython runtime.")

        logger.info(f"Processing Flask app {app.name}...")
        process_flask_app(app, use_lib)
        logger.info("Finished processing Flask app.")

    logger.info("Finished processing the app.")

    return app


# Helper variables for processing various apps with default configurations.


def create_echo_app(faasm: bool = False) -> Flask:
    return _create_app(echo_app, use_faasm=faasm, use_lib=False)


def create_simple_app(faasm: bool = False) -> Flask:
    return _create_app(simple_app, use_faasm=faasm, use_lib=False)


def create_pyperformance_app(faasm: bool = False) -> Flask:
    return _create_app(pyperformance_app, use_faasm=faasm, use_lib=True)
