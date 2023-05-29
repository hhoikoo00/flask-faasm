from flask import Flask, request

ECHO_HOST = "127.0.0.1"
ECHO_PORT = 1500


app = Flask(__name__)


@app.post("/")
def echo():
    data = request.get_data()
    return f"{data}"


if __name__ == "__main__":
    app.run(
        host=ECHO_HOST,
        port=ECHO_PORT,
        debug=True,
    )
