from pymongo import MongoClient
from urllib import quote_plus
from persons import PersonsClient
from deals import DealsClient
from transfers import TransfersClient
from accounts import AccountsClient

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
