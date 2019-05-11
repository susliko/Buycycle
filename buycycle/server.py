from flask import Flask
from flask import request
from flask import jsonify
from flask import session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_cors import CORS
from flask_json_schema import JsonSchema, JsonValidationError
import logging
import datetime
from logging.handlers import RotatingFileHandler
from buycycle.schemas import *
from buycycle.db.client import *
from buycycle.errors import *

app = Flask(__name__)
app.secret_key = 'super secret key'
CORS(app)
login_manager = LoginManager()
login_manager.init_app(app)
schema = JsonSchema(app)

ok_resp = {'status': 'ok'}


@login_manager.user_loader
def load_user(user_id):
    return auth_client.get_user(user_id)


def check_access(account, is_update_req):
    owner = account['owner']
    user = session.get('user_id')
    acc_mode = account['mode']
    if (acc_mode == 'private' or (is_update_req and acc_mode == 'publicRestricted')) and owner != user:
        raise AccessDeniedError


def check_access_by_acc_id(acc_id, is_update_req):
    account = accounts_client.get_by_id(acc_id)
    check_access(account, is_update_req)


# auth routes

@app.route('/api/register', methods=['POST'])
@schema.validate(auth_schema)
def register():
    body = request.get_json()
    if auth_client.register(body):
        user = load_user(body['login'])
        login_user(user)
        return jsonify(ok_resp)
    else:
        raise AlreadyRegisteredError


@app.route('/api/login', methods=['POST'])
@schema.validate(auth_schema)
def login():
    body = request.get_json()
    user = auth_client.get_user(body['login'])
    if user is not None and user.password == body['password']:
        login_user(user)
        auth_client.login(body['login'])
        return jsonify(ok_resp)
    else:
        raise LoginFailedError


@app.route('/api/logout', methods=['POST'])
def logout():
    auth_client.logout(session.get('user_id'))
    logout_user()
    return jsonify(ok_resp)


@app.route('/api/whoAmI', methods=['GET'])
def who_am_i():
    user = session.get('user_id')
    if user is not None:
        return jsonify({'isRegistered': True,
                        'userId': session['user_id']})
    else:
        return jsonify({'isRegistered': False,
                        'userId': 'you are nobody here!'})


# error handlers

@app.errorhandler(500)
def internal_error(e):
    return jsonify({"status": "internal_error",
                    "message": str(e)}), 400


@app.errorhandler(400)
def bad_request(e):
    return jsonify({"status": "bad_request",
                    "message": "why are you trying to kill my service? :("}), 400


@app.errorhandler(401)
def unauthorized(e):
    return jsonify({"status": "unauthorized",
                    "message": "login to perform this action"}), 401


@app.after_request
def attach_cors_headers(response):
    origin = request.headers.get('Origin')
    if origin is None:
        origin = '*'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'GET,HEAD,OPTIONS,POST,PUT,DELETE'
    response.headers['Access-Control-Allow-Origin'] = origin
    return response


app.register_error_handler(400, bad_request)
app.register_error_handler(401, unauthorized)
app.register_error_handler(500, internal_error)


@app.errorhandler(AccessDeniedError)
def access_denied_error(e):
    return jsonify({'status': e.message}), 401


@app.errorhandler(JsonValidationError)
def validation_error(e):
    return jsonify({'status': e.message, 'errors': [err.message for err in e.errors]}), 400


@app.errorhandler(AlreadyRegisteredError)
def registration_error(e):
    return jsonify({'status': e.status, 'message': e.message}), 400


@app.errorhandler(LoginFailedError)
def login_error(e):
    return jsonify({'status': e.status, 'message': e.message})


@app.route("/")
def hello():
    return "<h1 style='color:blue'>I want to ride my buycycle, I want to ride my bike!</h1>"


# persons CRUD


@app.route('/api/addPerson', methods=['POST'])
@schema.validate(person_schema)
def add_person():
    body = request.get_json()
    body['owner'] = session.get('user_id')
    check_access_by_acc_id(body['accountId'], True)
    body['login'] = session.get('user_id')
    return jsonify(persons_client.add(body))


@app.route('/api/updatePerson', methods=['POST'])
@schema.validate(person_schema)
def update_person():
    per_id = request.args.get("personId")
    body = request.get_json()
    check_access_by_acc_id(body['accountId'], True)
    return jsonify(persons_client.update_by_id(per_id, body))


@app.route('/api/getPersons', methods=['GET'])
def get_persons():
    acc_id = request.args.get("accountId")
    check_access_by_acc_id(acc_id, False)
    res = persons_client.get_by_acc_id(acc_id)
    return jsonify(persons_debts_enrichment(res, acc_id))


def persons_debts_enrichment(persons_list, account_id):
    optimized_debts = debts_client.get_optimized_debts(account_id)
    for debt in optimized_debts:

        for person in persons_list:
            if "debtors" not in person.keys():
                person["debtors"] = []
            if "lenders" not in person.keys():
                person["lenders"] = []

            if person["id"] == debt["sender"]:
                person["debtors"].append({"name": debt["receiver"],
                                          "amount": debt["amount"]})
            if person["id"] == debt["receiver"]:
                person["lenders"].append({"name": debt["sender"],
                                          "amount": debt["amount"]})
    return persons_list


# accounts CRUD

@app.route("/api/getAccounts", methods=['GET'])
@login_required
def get_accounts():
    return jsonify(accounts_client.get_accs_by_user(session.get('user_id')))


@app.route("/api/addAccount", methods=['POST'])
@schema.validate(account_schema)
@login_required
def add_account():
    body = request.get_json()
    body['createdAt'] = str(datetime.datetime.now())
    body['owner'] = session.get('user_id')
    return jsonify(accounts_client.add(body))


@app.route('/api/updateAccount', methods=['POST'])
@schema.validate(account_schema)
def update_account():
    acc_id = request.args.get("accountId")
    body = request.get_json()
    check_access_by_acc_id(acc_id, True)
    return jsonify(accounts_client.update_by_id(acc_id, body))


@app.route('/api/getAccount', methods=['GET'])
def get_account():
    acc_id = request.args.get("accountId")
    account = accounts_client.get_by_id(acc_id)
    check_access(account, False)
    return jsonify(account)


# transfers CRUD


@app.route("/api/addTransfer", methods=['POST'])
@schema.validate(transfer_schema)
def add_transfer():
    body = request.get_json()
    body['owner'] = session.get('user_id')
    check_access_by_acc_id(body['accountId'], True)
    debts_client.add_from_transfer(body)
    return jsonify(transfers_client.add(body))


@app.route('/api/updateTransfer', methods=['POST'])
@schema.validate(transfer_schema)
def update_transfer():
    tr_id = request.args.get("transferId")
    body = request.get_json()
    check_access_by_acc_id(body['accountId'], True)
    debts_client.update_from_transfer(tr_id, body)
    transfers_client.update_by_id(tr_id, body)
    return jsonify(ok_resp)


@app.route('/api/deleteTransfer', methods=['DELETE'])
def delete_transfer():
    tr_id = request.args.get("transferId")
    transfer = transfers_client.get_by_id(tr_id)
    check_access_by_acc_id(transfer['accountId'], True)
    debts_client.delete_from_transfer(tr_id)
    transfers_client.delete_by_id(tr_id)
    return jsonify(ok_resp)


@app.route('/api/getTransfers', methods=['GET'])
def get_transfers():
    acc_id = request.args.get("accountId")
    check_access_by_acc_id(acc_id, False)
    return jsonify(transfers_client.get_by_acc_id(acc_id))


# deals CRUD


@app.route("/api/addDeal", methods=['POST'])
@schema.validate(deal_schema)
def add_deal():
    body = request.get_json()
    body['owner'] = session.get('user_id')
    acc_id = body['accountId']
    check_access_by_acc_id(acc_id, True)
    debts_client.add_from_deal(body)
    return jsonify(deals_client.add(body))


@app.route('/api/updateDeal', methods=['POST'])
@schema.validate(deal_schema)
def update_deal():
    deal_id = request.args.get("dealId")
    body = request.get_json()
    check_access_by_acc_id(body['accountId'], True)
    debts_client.update_from_deal(deal_id, body)
    deals_client.update_by_id(deal_id, body)
    return jsonify(ok_resp)


@app.route('/api/deleteDeal', methods=['DELETE'])
def delete_deal():
    deal_id = request.args.get("dealId")
    deal = deals_client.get_by_id(deal_id)
    check_access_by_acc_id(deal['accountId'], True)
    debts_client.delete_from_deal(deal_id)
    deals_client.delete_by_id(deal_id)
    return jsonify(ok_resp)


@app.route('/api/getDeals', methods=['GET'])
def get_deals():
    acc_id = request.args.get("accountId")
    check_access_by_acc_id(acc_id, False)
    return jsonify(deals_client.get_by_acc_id(acc_id))


@app.route('/api/getDebts', methods=['GET'])
def get_debts():
    acc_id = request.args.get("accountId")
    check_access_by_acc_id(acc_id, False)
    return jsonify(debts_client.get_by_acc_id(acc_id))


if __name__ == "__main__":
    formatter = logging.Formatter(
        "[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
    log_handler = RotatingFileHandler('logs/buycycle.log', maxBytes=100000, backupCount=1)
    log_handler.setLevel(logging.DEBUG)
    log_handler.setFormatter(formatter)

    log = logging.getLogger('werkzeug')
    log.setLevel(logging.DEBUG)

    app.logger.addHandler(log_handler)
    log.addHandler(logging.StreamHandler())
    log.addHandler(log_handler)

    app.run(host='0.0.0.0', port=8000)

