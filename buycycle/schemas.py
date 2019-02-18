account_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "persons": {"type": "array",
                    "items": {
                        "type": "string"}},
        "deals": {"type": "array",
                  "items": {
                      "type": "string"}},
        "transfers": {"type": "array",
                      "items": {
                          "type": "string"}}
    },
    "required": ["name"]
}

person_schema = {
    "type": "object",
    "properties": {
        "account_id": {"type": "string"},
        "name": {"type": "string"},
        "debtors": {"type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "amount": {"type": "string"}
                        },
                        "required": ["name", "amount"]}},
        "lenders": {"type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "amount": {"type": "string"}
                        },
                        "required": ["name", "amount"]}}
    },
    "required": ["account_id", "name"]
}

deal_schema = {
    "type": "object",
    "properties": {
        "account_id": {"type": "string"},
        "name": {"type": "string"},
        "lender": {"type": "string"},
        "members": {"type": "array",
                    "items": {
                        "type": "string"}},
        "type": {"enum": ["oneForAll"]}
    },
    "required": ["account_id", "name", "lender", "members", "type"]
}

transfer_schema = {
    "type": "object",
    "properties": {
        ""
        "sender": {"type": "string"},
        "receiver": {"type": "string"},
        "amount": {"type": "number"},
        "currency": {"type": "string"}
    },
    "required": ["sender", "receiver", "amount", "currency"]
}

