from flask import Flask

from .lib.chaos import run_chaos

app = Flask(__name__)


@app.post("/bm/chaos")
def chaos():
    run_chaos()
    return "Success"
