from pymongo import MongoClient

uri = "mongodb+srv://admin:admin@c4e29-cluster-qtb0x.mongodb.net/test?retryWrites=true"

client = MongoClient(uri)

foods_db = client.project_database

Foods = foods_db["food_collection"]
Users = foods_db["users"]

