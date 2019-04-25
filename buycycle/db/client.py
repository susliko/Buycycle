from pymongo import MongoClient
from urllib.parse import quote_plus
from buycycle.db.persons import PersonsClient
from buycycle.db.deals import DealsClient
from buycycle.db.transfers import TransfersClient
from buycycle.db.accounts import AccountsClient
from buycycle.db.debts import DebtsClient
from buycycle.db.auth import AuthClient

user = "admin"  # TODO from environment
password = "MVSdiht"  # TODO
host = "199.247.6.17"  # TODO
uri = "mongodb://%s:%s@%s" % (quote_plus(user), quote_plus(password), host)

client = MongoClient(uri)
db = client.buycycle

persons_client = PersonsClient(db.persons)
deals_client = DealsClient(db.deals)
transfers_client = TransfersClient(db.transfers)
accounts_client = AccountsClient(db.accounts)
debts_client = DebtsClient(db.debts)
auth_client = AuthClient(db.auth)
