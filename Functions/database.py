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
