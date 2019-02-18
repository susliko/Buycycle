from flask import Flask
from flask import request
from flask import jsonify
from flask_json_schema import JsonSchema, JsonValidationError
from buycycle.schemas import *
from buycycle.db.client import *

app = Flask(__name__)
schema = JsonSchema(app)

error_msg = "you're dick who's trying to kill my service"


def error_resp(msg):
    return jsonify({"status": "error",
                    "message": msg})


def cond_error_resp(cond, msg):
    if cond:
        error_resp(msg)


@app.errorhandler(JsonValidationError)
def validation_error(e):
    return jsonify({'error': e.message, 'errors': [err.message for err in e.errors]})


@app.route("/")
def hello():
    return "<h1 style='color:blue'>Hello Masha!</h1>"


@app.route('/api/addPerson', methods=['POST'])
@schema.validate(add_person_req)
def add_person():
    body = request.get_json()
    cond_error_resp(body is None, error_msg)
    return jsonify(persons_client.add(body['name']))


@app.route("/api/addAccount", methods=['POST'])
@schema.validate(add_account_req)
def add_account():
    return error_msg


@app.route("/api/addTransfer", methods=['POST'])
@schema.validate(add_transfer_req)
def add_transfer():
    return error_msg


@app.route("/api/addDeal", methods=['POST'])
@schema.validate(add_deal_req)
def add_deal():
    return error_msg


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)

