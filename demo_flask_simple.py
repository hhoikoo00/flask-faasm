import argparse
import logging

from flask import Flask

from lib.flask import process_flask_app
from webapp import simple_app

logger = logging.getLogger(__name__)

APP_OBJECT_MAP = {"simple_app": simple_app}


def demo_flask_faasm(app: Flask, host: str, port: int) -> None:
    process_flask_app(app)

    # Launch the modified webapp.
    app.run(
        host=host,
        port=port,
        debug=True,
    )


def main() -> None:
    logging.basicConfig(level=logging.INFO)

    # Parse command-line arguments.
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--app", type=str, default="simple_app", help="Name of the webapp to demo with.")
    arg_parser.add_argument("--host", type=str, default="127.0.0.1", help="Host to run the webapp on.")
    arg_parser.add_argument(
        "--port", type=int, default=8000, help="Port to run the webapp on. Avoid 8002 and 8080 as Faasm uses it."
    )
    args = arg_parser.parse_args()

    app_str: str = args.app
    if app_str not in APP_OBJECT_MAP:
        error_msg = f"Given --app={app_str!r} does not exist! Choose from one of: {tuple(APP_OBJECT_MAP)}."
        logger.error(error_msg)
        raise FileNotFoundError(error_msg)
    app = APP_OBJECT_MAP[app_str]
    host: str = args.host
    port: int = args.port

    # Run the demo with given `app`.
    demo_flask_faasm(app, host, port)


if __name__ == "__main__":
    main()
