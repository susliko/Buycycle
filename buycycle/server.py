from flask import Flask
from flask import request
from flask import jsonify
from flask_json_schema import JsonSchema, JsonValidationError
from buycycle.schemas import *
from buycycle.db.client import *

app = Flask(__name__)
schema = JsonSchema(app)


@app.errorhandler(400)
def common_error(e):
    return jsonify({"status": "error",
                    "message": "why are you trying to kill my service? :("}), 400


app.register_error_handler(400, common_error)


@app.errorhandler(JsonValidationError)
def validation_error(e):
    return jsonify({'error': e.message, 'errors': [err.message for err in e.errors]}), 400


@app.route("/")
def hello():
    return "<h1 style='color:blue'>I want to ride my buycycle, I want to ride my bike!</h1>"


# persons CRUD


@app.route('/api/addPerson', methods=['POST'])
@schema.validate(person_schema)
def add_person():
    body = request.get_json()
    return jsonify(persons_client.add(body))


@app.route('/api/updatePerson', methods=['POST'])
@schema.validate(person_schema)
def update_person():
    per_id = request.args.get("personId")
    if per_id is None:
        return '', 400
    body = request.get_json()
    return jsonify(persons_client.update_by_id(per_id, body))


@app.route('/api/getPersons', methods=['GET'])
def get_persons():
    acc_id = request.args.get("accountId")
    res = persons_client.get_by_acc_id(acc_id)
    return jsonify(res)


# accounts CRUD


@app.route("/api/addAccount", methods=['POST'])
@schema.validate(account_schema)
def add_account():
    body = request.get_json()
    return jsonify(accounts_client.add(body))


@app.route('/api/updateAccount', methods=['POST'])
@schema.validate(account_schema)
def update_account():
    acc_id = request.args.get("personId")
    body = request.get_json()
    return jsonify(persons_client.update_by_id(acc_id, body))


@app.route('/api/getAccount', methods=['GET'])
def get_account():
    acc_id = request.args.get("accountId")
    return jsonify(accounts_client.get_by_acc_id(acc_id))


# transfers CRUD


@app.route("/api/addTransfer", methods=['POST'])
@schema.validate(transfer_schema)
def add_transfer():
    body = request.get_json()
    debts_client.add_from_transfer(body)
    return jsonify(transfers_client.add(body))


@app.route('/api/updateTransfer', methods=['POST'])
@schema.validate(transfer_schema)
def update_transfer():
    tr_id = request.args.get("transferId")
    body = request.get_json()
    debts_client.update_from_transfer(tr_id, body)
    transfers_client.update_by_id(tr_id, body)
    return '', 204


@app.route('/api/deleteTransfer', methods=['DELETE'])
def delete_transfer():
    tr_id = request.args.get("transferId")
    debts_client.delete_from_transfer(tr_id)
    transfers_client.delete_by_id(tr_id)
    return '', 204


@app.route('/api/getTransfers', methods=['GET'])
def get_transfers():
    tr_id = request.args.get("accountId")
    if tr_id is None:
        return '', 400
    return jsonify(transfers_client.get_by_acc_id(tr_id))


# deals CRUD


@app.route("/api/addDeal", methods=['POST'])
@schema.validate(deal_schema)
def add_deals():
    body = request.get_json()
    debts_client.add_from_deal(body)
    return jsonify(deals_client.add(body))


@app.route('/api/updateDeal', methods=['POST'])
@schema.validate(deal_schema)
def update_deal():
    deal_id = request.args.get("dealId")
    body = request.get_json()
    debts_client.update_from_deal(deal_id, body)
    persons_client.update_by_id(deal_id, body)
    return '', 204


@app.route('/api/deleteDeal', methods=['DELETE'])
def delete_deal():
    deal_id = request.args.get("dealId")
    debts_client.delete_from_deal(deal_id)
    deals_client.delete_by_id(deal_id)
    return '', 204


@app.route('/api/getDeals', methods=['GET'])
def get_deals():
    acc_id = request.args.get("accountId")
    return jsonify(transfers_client.get_by_acc_id(acc_id))


@app.route('/api/getDebts', methods=['GET'])
def get_debts():
    acc_id = request.args.get("accountId")
    return jsonify(debts_client.get_by_acc_id(acc_id))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)

