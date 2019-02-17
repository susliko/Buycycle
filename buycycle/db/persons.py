from base import CollManager


class PersonsClient(CollManager):

    def add(self, name):
        return {"id": str(self.client.insert_one({"name": name}).inserted_id)}
