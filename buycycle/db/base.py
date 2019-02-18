class CollManager:
    def __init__(self, client):
        self.client = client

    def get_by_id(self, doc_id):
        entry = self.client.find_one({"_id": doc_id})
        entry.update({'id': str(entry['_id'])})
        del entry['_id']
        return entry

    def add(self, body):
        return {"id": str(self.client.insert_one(body).inserted_id)}
