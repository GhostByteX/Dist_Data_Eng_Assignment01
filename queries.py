import datetime
import random
import string
from pymongo import MongoClient
import pymongo
import pandas as pd

# Establish connection to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["social_network"]

# All posts of a user
def get_user_posts(user_id):
    posts = list(db.posts.find({"user_id": user_id}))
    return posts

# Top k most liked posts of a user
def get_top_liked_posts(user_id, k):
    posts = list(db.posts.find({"user_id": user_id}).sort([("likes_count", pymongo.DESCENDING)]).limit(k))
    return posts

# Top k most commented posts of a user
def get_top_commented_posts(user_id, k):
    posts = list(db.posts.find({"user_id": user_id}).sort([("comments_count", pymongo.DESCENDING)]).limit(k))
    return posts

# All comments of a user
def get_user_comments(user_id):
    comments = list(db.posts.aggregate([
        {"$unwind": "$comments"},
        {"$match": {"comments.user_id": user_id}},
        {"$project": {"_id": 0, "post_id": "$_id", "comment": "$comments"}}
    ]))
    return comments

# All posts on a topic
def get_posts_by_topic(topic):
    posts = list(db.posts.find({"topic": topic}))
    return posts

# Top k most popular topics in terms of posts
def get_top_topics(k):
    topics = list(db.posts.aggregate([
        {"$group": {"_id": "$topic", "count": {"$sum": 1}}},
        {"$sort": {"count": pymongo.DESCENDING}},
        {"$limit": k}
    ]))
    return topics

# Posts of all friends in last 24 hours
def get_friends_posts_last_24_hours(user_id):
    friends = db.users.find_one({"_id": user_id})["friends"]
    posts = list(db.posts.find({
        "user_id": {"$in": friends},
        "createdAt": {"$gt": datetime.datetime.utcnow() - datetime.timedelta(hours=24)}
    }))
    return posts


def get_choice ():
    choice = int(input("\n1)All posts of user\n2)Top k most liked posts of user\n3)Top k most commented posts of user\n4)All comments of user\n5)All posts on topic\n6)Top k most popular topics in terms of posts\n7)Posts of all friends of user in last 24 hours\n8)Exit\n\n  "))

    while choice < 1 or choice > 8:
        print("\n\nInvalid option chosen, Try Again\n\n")
        choice = int(input("\n1)All posts of user\n2)Top k most liked posts of user\n3)Top k most commented posts of user\n4)All comments of user\n5)All posts on topic\n6)Top k most popular topics in terms of posts\n7)Posts of all friends of user in last 24 hours\n\n  "))
    return choice
# Run the queries and output the results to the console






def execute_queries():


    choice = 0

    while choice != 8:

        choice = get_choice()

        if choice == 1:
            
            user_id = input("Enter the user ID (e.g 'user21')\n")
            print(f"All posts of user {user_id}:")
            result = get_user_posts(user_id)
            print(result)
            print("TOTAL RESULTS FOUND:  \n",len(result))
            
            df = pd.DataFrame(result)
            df = df.drop(df.columns[0],axis=1)
            df.to_csv("results\\posts_userID.csv")
            
        elif choice == 2:
            
            user_id = input("Enter the user ID (e.g 'user21')\n")
            k = int(input("Enter the value of k\n"))
            print(f"Top {k} most liked posts of user {user_id}:")
            result = get_top_liked_posts(user_id, k)
            print(result)
            print("TOTAL RESULTS FOUND:  \n",len(result))
            
            df = pd.DataFrame(result)
            df = df.drop(df.columns[0],axis=1)
            df.to_csv("results\\k_liked_posts_userID.csv")

        elif choice == 3:
            
            user_id = input("Enter the user ID (e.g 'user21')\n")
            k = int(input("Enter the value of k\n"))
            print(f"Top {k} most commented posts of user {user_id}:")
            result = get_top_commented_posts(user_id, k)
            print(result)
            print("TOTAL RESULTS FOUND:  \n",len(result))
            
            df = pd.DataFrame(result)
            df = df.drop(df.columns[0],axis=1)
            df.to_csv("results\\k_commented_posts_userID.csv")

        elif choice == 4:
            
            user_id = input("Enter the user ID (e.g 'user21')\n")
            print(f"All comments of user {user_id}:")
            result = get_user_comments(user_id)
            print(result)
            print("TOTAL RESULTS FOUND:  \n",len(result))
            
            df = pd.DataFrame(result)
            df = df.drop(df.columns[0],axis=1)
            df.to_csv("results\\all_comments_user.csv")


        elif choice == 5:
            
            topic = input("Enter the topic\n")
            print(f"All posts on topic {topic}:")
            result = get_posts_by_topic(topic)
            print(result)
            print("TOTAL RESULTS FOUND:  \n",len(result))
            
            df = pd.DataFrame(result)
            df = df.drop(df.columns[0],axis=1)
            df.to_csv("results\\all_posts_topic.csv")
            
        elif choice == 6:
            
            k = int(input("Enter the value of k\n"))
            print(f"Top {k} most popular topics in terms of posts:")
            result = get_top_topics(k)
            print(result)
            print("TOTAL RESULTS FOUND:  \n",len(result))
            
            df = pd.DataFrame(result)
            df = df.drop(df.columns[0],axis=1)
            df.to_csv("results\\k_popular_topics.csv")
           

        elif choice == 7:
            
            user_id = input("Enter the user ID (e.g 'user21')\n")
            print(f"Posts of all friends of user {user_id} in last 24 hours:")
            result = get_friends_posts_last_24_hours(user_id)
            print(result)
            print("TOTAL RESULTS FOUND:  \n",len(result))
            
            df = pd.DataFrame(result)
            df.to_csv("results\\posts_by_friends_within_24hrs.csv")
            
        elif choice == 8:
            print("\nThank you! GoodBye\n\n")
            exit()
            
        else:
            print("\n\nInvalid Choice\n\n")
            
if __name__=='__main__':
    execute_queries()