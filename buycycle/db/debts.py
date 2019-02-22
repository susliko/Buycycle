from buycycle.db.base import CollManager
from buycycle.db import client


class DebtsClient(CollManager):

    def add_from_transfer(self, body):
        debt = self.find_debt(body)
        if debt is None:
            self.client.insert_one(body)
        else:
            self.change_record(body, debt)

    def add_from_deal(self, body):
        if body["type"] == "oneForAll":
            members = body["members"]
            for member in members:
                if member == body["lender"]:
                    continue
                new_transfer = {"sender": body["lender"],
                                "receiver": member,
                                "amount": body["amount"]/len(members)}
                print(new_transfer)
                self.add_from_transfer(new_transfer)


    def update_from_transfer(self, transfer_id, body):
        transfer = client.transfers_client.get_by_id(transfer_id)
        new_transfer = body

        if body["sender"] == transfer["sender"]:
            if body["amount"] >= transfer["amount"]:
                new_transfer["amount"] = body["amount"] - transfer["amount"]
            else:
                new_transfer["sender"] = body["receiver"]
                new_transfer["receiver"] = body["sender"]
                new_transfer["amount"] = transfer["amount"] - body["amount"]
        else:
            new_transfer["sender"] = body["receiver"]
            new_transfer["receiver"] = body["sender"]
            new_transfer["amount"] = transfer["amount"] + body["amount"]

        self.add_from_transfer(new_transfer)

    def find_debt(self, body):
        return self.client.find_one({"accountId": body["accountId"],
                                     "$or": [{"sender": body["sender"],
                                              "receiver": body["receiver"]},
                                             {"receiver": body["sender"],
                                              "sender": body["receiver"]}]})

    def change_record(self, transfer, debt):
        if transfer["sender"] == debt["sender"]:
            debt["amount"] = debt["amount"] + transfer["amount"]
            self.client.update_one({"_id": debt["_id"]}, {"$set": debt})
        else:
            if debt["amount"] > transfer["amount"]:
                debt["amount"] = debt["amount"] - transfer["amount"]
                self.client.update_one({"_id": debt["_id"]}, {"$set": debt})
            elif debt["amount"] == transfer["amount"]:
                self.client.delete_one({"_id": debt["_id"]})
            else:
                debt["sender"] = transfer["sender"]
                debt["receiver"] = transfer["receiver"]
                debt["amount"] = transfer["amount"] - debt["amount"]

                self.client.update_one({"_id": debt["_id"]}, {"$set": debt})
