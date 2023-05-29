from http.client import HTTPResponse
from urllib.request import Request, urlopen

from flask import Flask, request

app = Flask(__name__)


@app.get("/value")
def value():
    return "42"


@app.get("/user/<int:user_id>")
def user(user_id: int):
    return f"User {user_id} given!"


@app.get("/user/<int:user_id>/<username>")
def user_detail(user_id: int, username: str):
    return f"User {user_id} has {username=}"


@app.post("/user/form")
def user_form_stuff():
    username, password = request.form["username"], request.form["password"]
    return f"{username=}, {password=}"


@app.post("/data/parse")
def request_body_stuff():
    assert request.method == "POST"
    if request.is_json:
        request_body = request.json
    else:
        request_body = request.get_data()
    return f"Body of the request given was {request_body}"


@app.post("/http/echo")
def make_http_request_to_echo():
    """
    Demo showing how HTTP request should be made in a Faasm environment.
    User must ensure that the echo webapp must be hosted (at `./webapp/echo/app.py`).
    """

    ECHO_HOST = "http://127.0.0.1"
    ECHO_PORT = 1500
    ECHO_ENDPOINT = ""

    # Encode the data into bytes. `as_text` flag purposefully used to emphasise that
    # the data needs to be encoded into bytes for the constructor of Request() object.
    data_str = request.get_data(as_text=True)
    data = data_str.encode(encoding="utf-8")

    echo_request = Request(f"{ECHO_HOST}:{ECHO_PORT}/{ECHO_ENDPOINT}", data=data)
    echo_response: HTTPResponse
    with urlopen(echo_request) as echo_response:
        data = echo_response.read()
        data_str = data.decode(encoding="utf-8")

    return data
