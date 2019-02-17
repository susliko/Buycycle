addAccountReq = {
    "type": "object",
    "properties" :{
        "name": {"type": "string"}
    }
}

addPersonReq = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "name": {"type": "string"}
    }
}

addDealReq = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "name": {"type": "string"},
        "lender": {"type": "string"},
        "members": {"type": "array",
                    "items": {
                        "type": "string"}},
        "type": {"enum": ["oneForAll"]}
    }
}

addTransferReq = {
    "type": "object",
    "properties": {
        "sender": {"type": "string"},
        "receiver": {"type": "string"},
        "amount": {"type": "number"},
        "currency": {"type": "string", "optional": True}
    }
}

