import os
import pymongo as pymongo

client = pymongo.MongoClient(os.getenv('database_access'))
# print(client)
database_to_connect = "MerotiBot"
db = client[database_to_connect]
# print(db)
server_collection = db["servers"]


def get_response(response):
    channel_got = f"{response}"
    prettified = channel_got.split(":")
    prettified = prettified[1].replace("}", "")
    prettified = prettified.replace(" ", "")
    prettified = prettified.replace("'", "")
    prettified = prettified.replace('"', "")
    return prettified


def add_for_all(key, initial_value):
    server_collection.update_many({}, {"$set": {f"{key}": initial_value}}, upsert=True)
    print(f"Updated: {key}: {initial_value}")


def add_for_one(server_id, key, value):
    server_collection.update_one({"guild id": server_id}, {"$set": {f"{key}": value}})
    print(f"Updated: {key}: {value}")
