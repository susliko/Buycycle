from flask import Flask
from flask import request
from flask import jsonify
import jsonschema
from jsonschema import validate
from schemas import *
from client import *

app = Flask(__name__)

error_msg = "you're dick who's trying to kill my service"


def error_resp(msg):
    return jsonify({"status": "error",
                    "message": msg})


def cond_error_resp(cond, msg):
    if cond:
        error_resp(msg)


@app.route("/")
def hello():
    return "<h1 style='color:blue'>Hello Masha!</h1>"


@app.route("/api/addPerson", methods=['POST'])
def add_person():
    body = request.get_json()
    cond_error_resp(body is None, error_msg)
    try:
        validate(body, addPersonReq)
    except jsonschema.exceptions.ValidationError as ve:
        error_resp(str(ve))
    return jsonify(persons_client.add(body['name']))


@app.route("/api/addAccount", methods=['POST'])
def add_account():
    return error_msg


@app.route("/api/addTransfer", methods=['POST'])
def add_transfer():
    return error_msg


@app.route("/api/addDeal", methods=['POST'])
def add_deal():
    return error_msg


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)

