from pymongo import MongoClient


def get_mongodb():
    client = MongoClient("mongodb+srv://andreshizap:567234@cluster0.pqxcf.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    db = client.hw
    return db