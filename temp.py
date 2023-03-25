import datetime
import random
import string
from pymongo import MongoClient

client = MongoClient("mongodb+srv://usmanmalik740:Usmanmalik8058@cluster0.uu0bwxt.mongodb.net/?retryWrites=true&w=majority")
# db = client.test

db = client['social_network']

shards = db.command('listShards')['shards']

# Access the first three shards
for i in range(3):
    shard_uri = shards[i]['host']
    print(f"Accessing shard {i+1} with URI: {shard_uri}")
    shard_client = MongoClient(f"mongodb://{shard_uri}")
    shard_db = shard_client['social_network']
    # Perform operations on the shard_db as needed