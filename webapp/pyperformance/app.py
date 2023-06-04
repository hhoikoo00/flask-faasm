from flask import Flask

from .lib.chaos import bench_chaos

app = Flask(__name__)


@app.post("/bm/chaos")
def chaos():
    bench_chaos()
    return "Success"
