from pymongo.collection import Collection


def remove_by_key(coll: Collection, key: str):
    coll.delete_many({'key': key})
