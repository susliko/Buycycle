from bson import ObjectId
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

    def add(self, body):
        return {"id": str(self.client.insert_one(body).inserted_id)}
