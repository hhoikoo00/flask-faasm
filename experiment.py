"""
Module containing various webapps that are used in the experiments.
Set the `FAASM` environment variable to enable Faasm processing.
The apps are expected to be run with `gunicorn`. Configuration file in `./gunicorn.conf.py`.
It is also expected that the apps would be run on a 'production' level.

Usage:
* If Faasm processing should be disabled.
    * `gunicorn 'experiment:<app-name>'`
* If Faasm processing should be enabled.
    * `FAASM= gunicorn 'experiment:<app-name>' `
"""


import os

from lib.faasm import upload_cpython_runtime
from lib.flask import process_flask_app
from webapp import echo_app, simple_app  # type: ignore

# Determine if the apps for the experiment should be run with Faasm processing enabled.
USE_FAASM = "FAASM" in os.environ


# Upload the CPython runtime if Faasm should be used for the experiment.
if USE_FAASM:
    upload_cpython_runtime()


# Set apps that could be processed into Faasm apps.
# This is used mainly to disable unnecessary processing if the app doesn't need to be procees
ENABLED_APPS = {
    simple_app,
}


# Process the Flask app if `USE_FAASM` is enabled.
if USE_FAASM:
    for app in ENABLED_APPS:
        process_flask_app(app)
