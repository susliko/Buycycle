from buycycle.db.base import CollManager
from buycycle.utils import *


class AccountsClient(CollManager):

    def get_accs_by_user(self, user):
        return list(map(lambda x: object_id_to_str(x),
                        list(self.client.find({"owner": user}))))

