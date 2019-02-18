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
@schema.validate(person_schema)
def add_person():
    body = request.get_json()
    return jsonify(persons_client.add(body['name']))


@app.route("/api/addAccount", methods=['POST'])
@schema.validate(account_schema)
def add_account():
    body = request.get_json()
    return jsonify(accounts_client.add(body))


@app.route("/api/addTransfer", methods=['POST'])
@schema.validate(transfer_schema)
def add_transfer():
    body = request.get_json()
    return jsonify(transfers_client.add(body))


@app.route("/api/addDeal", methods=['POST'])
@schema.validate(deal_schema)
def add_deal():
    body = request.get_json()
    return jsonify(deals_client.add(body))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)

