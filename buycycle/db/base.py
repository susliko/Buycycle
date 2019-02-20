from bson.objectid import ObjectId
from buycycle.utils import object_id_to_str


class CollManager:
    def __init__(self, client):
        self.client = client

    def get_by_id(self, doc_id):
        entry = self.client.find_one({"_id": ObjectId(doc_id)})
        if entry is None:
            return None
        object_id_to_str(entry)
        return entry

    def get_by_acc_id(self, acc_id):
        return list(map(lambda x: object_id_to_str(x),
                        list(self.client.find({"accountId": acc_id}))))

    def add(self, body):
        return {"id": str(self.client.insert_one(body).inserted_id)}

    def update_by_id(self, doc_id, body):
        self.client.update_one({"_id": ObjectId(doc_id)}, {"$set": body})

    def delete_by_id(self, doc_id):
        self.client.delete_one({"_id": ObjectId(doc_id)})
