from buycycle.db.base import CollManager


class DealsClient(CollManager):

    def add(self, name, price, lender, members, type):
        return {"id": str(self.client.insert_one({"name": name,
                                                  "price": price,
                                                  "lender": lender,
                                                  "members": members,
                                                  "type": type}))}
