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
