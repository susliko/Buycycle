from buycycle.db.base import CollManager


class AccountsClient(CollManager):

    def add(self, name, persons=[], deals=[], transfers=[]):
        return {"id": str(self.client.insert_one({"name": name,
                                                  "persons": persons,
                                                  "deals": deals,
                                                  "transfers": transfers}))}
