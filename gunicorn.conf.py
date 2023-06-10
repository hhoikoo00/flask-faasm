import os
from multiprocessing import cpu_count

HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", "8000"))
bind = [f"{HOST}:{PORT}"]

# https://docs.gunicorn.org/en/stable/design.html#how-many-workers
workers = cpu_count() * 2 + 1

# Prevent workers from getting killed during upload of CPython binary.
timeout = 120

# Prevent the app from being processed multiple times.
preload_app = True

# Don't limit the size of the request made from gunicorn to Faasm.
limit_request_line = 0
