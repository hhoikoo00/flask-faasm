import argparse
import logging

from flask import Flask

from lib.flask import process_flask_app
from webapp import simple_app

logger = logging.getLogger(__name__)

APP_OBJECT_MAP = {"simple_app": simple_app}


def demo_flask_faasm(app: Flask) -> None:
    process_flask_app(app)

    # Launch the modified webapp.
    app.run(
        host="0.0.0.0",
        port=8000,
        debug=True,
    )


def main() -> None:
    logging.basicConfig(level=logging.INFO)

    # Parse command-line arguments.
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--app", type=str, default="simple_app", help="Name of the webapp to demo with.")
    args = arg_parser.parse_args()

    app_str: str = args.app
    if app_str not in APP_OBJECT_MAP:
        error_msg = f"Given --app={app_str!r} does not exist! Choose from one of: {tuple(APP_OBJECT_MAP)}."
        logger.error(error_msg)
        raise FileNotFoundError(error_msg)
    app = APP_OBJECT_MAP[app_str]

    # Run the demo with given `app`.
    demo_flask_faasm(app)


if __name__ == "__main__":
    main()
