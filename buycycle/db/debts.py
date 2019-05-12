from buycycle.db.base import CollManager
from buycycle.db import client
import operator


class DebtsClient(CollManager):

    precision = 10

    def add_from_transfer(self, body):
        debt = self.find_debt(body)
        if debt is None:
            self.client.insert_one(body)
        else:
            self.change_record(body, debt)

    def add_from_deal(self, body):
        if body["type"] == "OneForAll":
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

        if deal["type"] == "OneForAll":
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
            debt["amount"] = round(debt["amount"] + transfer["amount"], DebtsClient.precision)
            self.client.update_one({"_id": debt["_id"]}, {"$set": debt})
        else:
            if round(debt["amount"], DebtsClient.precision) > round(transfer["amount"], DebtsClient.precision):
                debt["amount"] = round(debt["amount"] - transfer["amount"], DebtsClient.precision)
                self.client.update_one({"_id": debt["_id"]}, {"$set": debt})
            elif round(debt["amount"], DebtsClient.precision) == round(transfer["amount"], DebtsClient.precision):
                self.client.delete_one({"_id": debt["_id"]})
            else:
                debt["sender"] = transfer["sender"]
                debt["receiver"] = transfer["receiver"]
                debt["amount"] = round(transfer["amount"] - debt["amount"], DebtsClient.precision)

                self.client.update_one({"_id": debt["_id"]}, {"$set": debt})

    def get_lenders_and_debtors(self, account_id):
        debts = self.client.find({"accountId": account_id})
        lenders_debtors = {}
        for debt in debts:
            sender = debt["sender"]
            receiver = debt["receiver"]
            amount = debt["amount"]

            if sender in lenders_debtors.keys():
                lenders_debtors[sender] += amount
            else:
                lenders_debtors[sender] = amount

            if receiver in lenders_debtors.keys():
                lenders_debtors[receiver] -= amount
            else:
                lenders_debtors[receiver] = -amount

        keys = set()
        for key in lenders_debtors.keys():
            if round(lenders_debtors.get(key), DebtsClient.precision) == 0:
                keys.add(key)

        for key in keys:
            lenders_debtors.pop(key)

        return lenders_debtors

    def get_optimized_debts(self, account_id):
        lenders_debtors = self.get_lenders_and_debtors(account_id)
        sorted_lenders = sorted(lenders_debtors.items(), key=operator.itemgetter(1))
        sorted_lenders = [list(x) for x in sorted_lenders]
        result = []
        while len(sorted_lenders) > 0:
            if round(abs(sorted_lenders[0][1]), DebtsClient.precision) < round(abs(sorted_lenders[-1][1]), DebtsClient.precision):
                result.append({"sender": sorted_lenders[-1][0],
                               "receiver": sorted_lenders[0][0],
                               "amount": abs(sorted_lenders[0][1])})
                sorted_lenders[-1][1] += sorted_lenders[0][1]
                sorted_lenders.pop(0)
            else:
                result.append({"sender": sorted_lenders[-1][0],
                               "receiver": sorted_lenders[0][0],
                               "amount": abs(sorted_lenders[-1][1])})
                if round(abs(sorted_lenders[0][1]), DebtsClient.precision) == round(abs(sorted_lenders[-1][1]), DebtsClient.precision):
                    sorted_lenders.pop(0)
                    sorted_lenders.pop(len(sorted_lenders) - 1)
                else:
                    sorted_lenders[0][1] += sorted_lenders[-1][1]
                    sorted_lenders.pop(len(sorted_lenders) - 1)
        return result


