from pymongo import MongoClient

def get_mongo_client(host, port):
    return MongoClient(host, int(port))
