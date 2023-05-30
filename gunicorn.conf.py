import os
from multiprocessing import cpu_count

HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", "8000"))
bind = [f"{HOST}:{PORT}"]

# https://docs.gunicorn.org/en/stable/design.html#how-many-workers
workers = cpu_count() * 2 + 1
