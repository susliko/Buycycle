auth_schema = {
    "type": "object",
    "properties": {
        "login": {"type": "string"},
        "password": {"type": "string"}
    },
    "required": ["login", "password"],
    "additionalProperties": False
}

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
                          "type": "string"}},
        "owner": {"type": "string"}
    },
    "required": ["name", "owner"],
    "additionalProperties": False
}

person_schema = {
    "type": "object",
    "properties": {
        "accountId": {"type": "string"},
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
                        "required": ["name", "amount"]}},
        "owner": {"type": "string"}
    },
    "required": ["accountId", "name", "owner"],
    "additionalProperties": False
}

deal_schema = {
    "type": "object",
    "properties": {
        "accountId": {"type": "string"},
        "name": {"type": "string"},
        "lender": {"type": "string"},
        "members": {"type": "array",
                    "items": {
                        "type": "string"}},
        "amount": {"type": "number"},
        "type": {"enum": ["OneForAll"]},
        "owner": {"type": "string"}
    },
    "required": ["accountId", "name", "lender", "members", "amount", "type", "owner"],
    "additionalProperties": False
}

transfer_schema = {
    "type": "object",
    "properties": {
        "accountId": {"type": "string"},
        "sender": {"type": "string"},
        "receiver": {"type": "string"},
        "amount": {"type": "number"},
        "currency": {"type": "string"},
        "owner": {"type": "string"}
    },
    "required": ["accountId", "sender", "receiver", "amount", "owner"],
    "additionalProperties": False
}

debt_schema = {
    "type": "object",
    "properties": {
        "accountId": {"type": "string"},
        "sender": {"type": "string"},
        "receiver": {"type": "string"},
        "amount": {"type": "number"},
        "owner": {"type": "string"}
    },
    "required": ["accountId", "sender", "receiver", "amount", "owner"],
    "additionalProperties": False
}

