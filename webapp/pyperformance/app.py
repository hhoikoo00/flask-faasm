from flask import Flask, request

app = Flask(__name__)


@app.get("/value")
def value():
    assert request.method == "GET"
    return "42"
