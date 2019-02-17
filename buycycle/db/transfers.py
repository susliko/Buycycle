from base import CollManager


class TransfersClient(CollManager):

    def add(self, sender, receiver, currency, amount):
        return {"id": str(self.client.insert_one({"sender": sender,
                                                  "receiver": receiver,
                                                  "currency": currency,
                                                  "amount": amount}))}
