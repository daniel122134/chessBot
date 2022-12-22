import pymongo as pymongo
from bson import ObjectId

c = pymongo.MongoClient(
    "mongodb+srv://barbot:barbot122@barbot.ury12.mongodb.net/barbot?retryWrites=true&w=majority", tlsAllowInvalidCertificates=True)
db = c.barbot


def find(collection, query_dict):
    result = [res for res in db[collection].find(query_dict)]
    for r in result:
        r["_id"] = str(r["_id"])
    return result


def find_one(collection, id):
    return db[collection].find_one({"_id": id})


def update(collection, query_dict, update_dict):
    return db[collection].update(query_dict, {"$set": update_dict})


def insert(collection, object):
    db[collection].insert_one(object)


def remove(collection, id):
    db[collection].delete_one({"_id": ObjectId(id)})
