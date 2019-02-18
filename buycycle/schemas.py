add_account_req = {
    "type": "object",
    "properties" :{
        "name": {"type": "string"}
    }
}

add_person_req = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "name": {"type": "string"}
    },
    "required": ["id", "name"]
}

add_deal_req = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "name": {"type": "string"},
        "lender": {"type": "string"},
        "members": {"type": "array",
                    "items": {
                        "type": "string"}},
        "type": {"enum": ["oneForAll"]}
    },
    "required": ["id", "name", "lender", "members", "type"]
}

add_transfer_req = {
    "type": "object",
    "properties": {
        "sender": {"type": "string"},
        "receiver": {"type": "string"},
        "amount": {"type": "number"},
        "currency": {"type": "string", "optional": True}
    },
    "required": ["sender", "receiver", "amount", "currency"]
}

