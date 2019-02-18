from buycycle.db.base import CollManager
from utils import object_id_to_str

class PersonsClient(CollManager):

    def get_by_acc_id(self, acc_id):
        return list(map(lambda x: object_id_to_str(x),
                        list(self.client.find({"account_id": acc_id}))))
