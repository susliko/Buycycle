from bson import ObjectId


def object_id_to_str(entry):
    entry.update({'id': str(entry['_id'])})
    del entry['_id']
    return entry


def str_to_object_id(entry):
    entry.update({'_id': ObjectId(entry['id'])})
    del entry['id']
    return entry
