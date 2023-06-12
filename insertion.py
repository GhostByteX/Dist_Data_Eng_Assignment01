import datetime
import random
import string
from pymongo import MongoClient

client = MongoClient("mongodb+srv://usmanmalik740:Usman740@cluster0.rpxlpvs.mongodb.net/social_network")

db = client.social_network

topics = ["Food", "Travel", "Technology", "Art", "Fashion", "Sports", "Music", "Politics", "Health", "Education"]



users = []
for i in range(3123):
    user_id = "user" + str(i)
    name = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=10))
    no_of_friends = random.randint(1,30)
    friends = random.sample(range(3123), no_of_friends)
    users.append({"_id": user_id, "name": name, "friends": friends})

db.users.insert_many(users)

posts = []
for i in range(19645):
    user = users[i % len(users)]
    topic = topics[random.randint(0,len(topics)-1)]

    post = {
        "user_id": user["_id"],
        "text": f"This is post number {i}",
        "topic": topic,
        "createdAt": datetime.datetime.now()-datetime.timedelta(days=(random.randint(0,1000)),hours=(random.randint(0,24)),minutes=(random.randint(0,59)),seconds=(random.randint(0,59)),milliseconds=(random.randint(0,999))),
        "likes": [],
        "comments": []
    }

    for j in range(len(users)//10):
        if random.random() < 0.5:
            post["likes"].append(users[j]["_id"])
        if random.random() < 0.5:
            comment = {
                "user_id": users[j]["_id"],
                "text": f"This is a comment by {users[j]['name']} on post {i}"
            }
            post["comments"].append(comment)
    posts.append(post)
 

db.posts.insert_many(posts)

db.posts.create_index("user_id")
db.posts.create_index("createdAt")
db.posts.create_index("topic")
db.users.create_index("name")

client.close()