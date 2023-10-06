from flask import Flask, request

from .helpers.handle_webhook import handle_webhook
from .helpers.verify_webhook import verify_webhook


app = Flask(__name__)

@app.route("/", methods=["get"])
def index():
    return "Ok", 200

@app.route("/mywebhook", methods=["get", "post"])
def my_webhook():
    if request.method == "GET":
        return verify_webhook(request)
    if request.method == "POST":
        return handle_webhook(request)


if(__name__) == "__main__":
    app.run(port=5000)