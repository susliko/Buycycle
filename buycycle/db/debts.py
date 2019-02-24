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
                new_transfer = {"accountId": body["accountId"],
                                "sender": body["lender"],
                                "receiver": member,
                                "amount": body["amount"]/len(members)}
                self.add_from_transfer(new_transfer)

    def delete_from_transfer(self, transfer_id):
        transfer = client.transfers_client.get_by_id(transfer_id)
        new_transfer = {"accountId": transfer["accountId"],
                        "sender": transfer["receiver"],
                        "receiver": transfer["sender"],
                        "amount": transfer["amount"]}

        self.add_from_transfer(new_transfer)

    def delete_from_deal(self, deal_id):
        deal = client.deals_client.get_by_id(deal_id)

        if deal["type"] == "oneForAll":
            members = deal["members"]
            for member in members:
                if member == deal["lender"]:
                    continue
                new_transfer = {"accountId": deal["accountId"],
                                "sender": member,
                                "receiver": deal["lender"],
                                "amount": deal["amount"]/len(members)}
                self.add_from_transfer(new_transfer)

    def update_from_deal(self, deal_id, body):
        self.delete_from_deal(deal_id)
        self.add_from_deal(body)

    def update_from_transfer(self, transfer_id, body):
        self.delete_from_transfer(transfer_id)
        self.add_from_transfer(body)

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
